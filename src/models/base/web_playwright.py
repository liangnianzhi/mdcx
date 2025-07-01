import asyncio
import json
import logging
from dataclasses import dataclass
from typing import List, Literal, Optional, Tuple
from urllib.parse import urljoin

from playwright.async_api import Browser, BrowserContext, Page, Playwright, async_playwright

from .utils import get_user_agent

logger = logging.getLogger(__name__)


@dataclass
class ProxyConfig:
    """代理配置"""

    server: str
    username: Optional[str] = None
    password: Optional[str] = None


@dataclass
class ViewportConfig:
    """视窗配置"""

    width: int = 1920
    height: int = 1080


@dataclass
class RequestOptions:
    """请求选项配置"""

    wait_for: Literal["load", "domcontentloaded", "networkidle", "commit"] = "domcontentloaded"
    wait_selector: Optional[str] = None  # 等待特定选择器出现
    wait_timeout: int = 10000  # 等待超时时间
    execute_js: Optional[str] = None  # 执行的JavaScript代码
    scroll_to_bottom: bool = False  # 是否滚动到底部
    screenshot: bool = False  # 是否截图，返回base64编码


@dataclass
class PostRequestOptions(RequestOptions):
    """POST请求选项配置"""

    data: Optional[dict] = None  # 表单数据
    json_data: Optional[dict] = None  # JSON数据


@dataclass
class PlaywrightConfig:
    """Playwright配置类"""

    # 浏览器配置
    headless: bool = True
    browser_type: str = "chromium"  # chromium, firefox, webkit
    slow_mo: int = 0  # 操作延迟毫秒数

    # 网络配置
    timeout: int = 30000  # 30秒超时
    user_agent: Optional[str] = None
    viewport: Optional[ViewportConfig] = None

    # 代理配置
    proxy: Optional[ProxyConfig] = None

    # 反检测配置
    stealth_mode: bool = True
    disable_images: bool = False  # 是否禁用图片加载
    disable_css: bool = False  # 是否禁用CSS加载
    block_ads: bool = True  # 是否屏蔽广告

    def __post_init__(self):
        """初始化后处理"""
        if self.user_agent is None:
            self.user_agent = get_user_agent()

        if self.viewport is None:
            self.viewport = ViewportConfig()


class PlaywrightBrowserManager:
    """Playwright浏览器管理器"""

    def __init__(self, config: Optional[PlaywrightConfig] = None):
        self.config = config or PlaywrightConfig()
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self._playwright: Optional[Playwright] = None

    async def start(self):
        """启动浏览器"""
        if self.browser:
            return

        self._playwright = await async_playwright().start()

        # 选择浏览器类型
        if self.config.browser_type == "firefox":
            browser_type = self._playwright.firefox
        elif self.config.browser_type == "webkit":
            browser_type = self._playwright.webkit
        else:
            browser_type = self._playwright.chromium

        # 启动浏览器
        browser_args = [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-blink-features=AutomationControlled",
            "--disable-features=VizDisplayCompositor",
        ]

        launch_kwargs = {
            "headless": self.config.headless,
            "slow_mo": self.config.slow_mo,
            "args": browser_args,
        }

        if self.config.proxy:
            proxy_settings = {"server": self.config.proxy.server}
            if self.config.proxy.username:
                proxy_settings["username"] = self.config.proxy.username
            if self.config.proxy.password:
                proxy_settings["password"] = self.config.proxy.password
            launch_kwargs["proxy"] = proxy_settings

        self.browser = await browser_type.launch(**launch_kwargs)

        # 创建上下文
        context_kwargs = {
            "user_agent": self.config.user_agent,
            "ignore_https_errors": True,
            "java_script_enabled": True,
        }

        # 添加视窗配置
        if self.config.viewport:
            context_kwargs["viewport"] = {"width": self.config.viewport.width, "height": self.config.viewport.height}

        self.context = await self.browser.new_context(**context_kwargs)

        # 启用隐身模式
        if self.config.stealth_mode:
            await self._setup_stealth_mode()

    async def _setup_stealth_mode(self):
        """设置反检测模式"""
        if not self.context:
            return

        # 添加初始化脚本，隐藏webdriver痕迹
        await self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            Object.defineProperty(navigator, 'languages', {
                get: () => ['zh-CN', 'zh', 'en'],
            });
            
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
            );
            
            window.chrome = {
                runtime: {},
            };
        """)

    async def stop(self):
        """停止浏览器"""
        if self.context:
            await self.context.close()
            del self.context

        if self.browser:
            await self.browser.close()
            del self.browser

        if self._playwright:
            await self._playwright.stop()
            del self._playwright

    async def new_page(self) -> Page:
        """创建新页面"""
        if not self.context:
            await self.start()

        page = await self.context.new_page()  # type: ignore

        # 设置默认超时
        page.set_default_timeout(self.config.timeout)

        # 设置资源过滤
        if self.config.disable_images or self.config.disable_css or self.config.block_ads:
            await page.route("**/*", self._handle_route)

        return page

    async def _handle_route(self, route):
        """处理请求路由，用于屏蔽资源"""
        request = route.request
        resource_type = request.resource_type
        url = request.url.lower()

        # 屏蔽图片
        if self.config.disable_images and resource_type == "image":
            await route.abort()
            return

        # 屏蔽CSS
        if self.config.disable_css and resource_type == "stylesheet":
            await route.abort()
            return

        # 屏蔽广告
        if self.config.block_ads and self._is_ad_url(url):
            await route.abort()
            return

        await route.continue_()

    def _is_ad_url(self, url: str) -> bool:
        """检测是否为广告URL"""
        ad_keywords = [
            "googleads",
            "googlesyndication",
            "doubleclick",
            "adsystem",
            "amazon-adsystem",
            "ads",
            "analytics",
            "facebook.com/plugins",
            "connect.facebook.net",
        ]
        return any(keyword in url for keyword in ad_keywords)


class PlaywrightRequester:
    """Playwright请求器"""

    def __init__(self, config: Optional[PlaywrightConfig] = None):
        self.config = config or PlaywrightConfig()
        self.manager = PlaywrightBrowserManager(self.config)

    async def get(self, url: str, options: Optional[RequestOptions] = None) -> Tuple[str, int]:
        """
        GET请求

        Args:
            url: 请求URL
            options: 请求选项配置

        Returns:
            Tuple[str, int]: (页面内容, 状态码)
        """
        if options is None:
            options = RequestOptions()

        page = None
        try:
            page = await self.manager.new_page()

            # 访问页面
            response = await page.goto(url, wait_until=options.wait_for)

            if not response:
                raise Exception("Failed to load page")

            # 等待特定选择器
            if options.wait_selector:
                await page.wait_for_selector(options.wait_selector, timeout=options.wait_timeout)

            # 滚动到底部（用于加载动态内容）
            if options.scroll_to_bottom:
                await self._scroll_to_bottom(page)

            # 执行JavaScript
            if options.execute_js:
                await page.evaluate(options.execute_js)

            # 获取页面内容
            content = await page.content()
            status_code = response.status

            return content, status_code

        except Exception as e:
            logger.error(f"Playwright request failed for {url}: {str(e)}")
            raise
        finally:
            if page:
                await page.close()

    async def post(self, url: str, options: Optional[PostRequestOptions] = None) -> Tuple[str, int]:
        """
        POST请求

        Args:
            url: 请求URL
            options: POST请求选项配置

        Returns:
            Tuple[str, int]: (响应内容, 状态码)
        """
        if options is None:
            options = PostRequestOptions()

        page = None
        try:
            page = await self.manager.new_page()

            # 设置POST数据
            if options.json_data:
                await page.set_extra_http_headers({"Content-Type": "application/json"})
                post_data = json.dumps(options.json_data)
            elif options.data:
                post_data = options.data
            else:
                post_data = ""

            # 执行POST请求
            response = await page.evaluate(f"""
                fetch('{url}', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: '{post_data}'
                }}).then(response => response.text())
            """)

            return response, 200

        except Exception as e:
            logger.error(f"Playwright POST request failed for {url}: {str(e)}")
            raise
        finally:
            if page:
                await page.close()

    async def _scroll_to_bottom(self, page: Page, delay: float = 1.0):
        """滚动到页面底部"""
        last_height = await page.evaluate("document.body.scrollHeight")

        while True:
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(delay)

            new_height = await page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    async def extract_text(
        self, url: str, selector: Optional[str] = None, options: Optional[RequestOptions] = None
    ) -> str:
        """
        提取页面文本内容

        Args:
            url: 请求URL
            selector: CSS选择器，如果指定则只提取该元素的文本
            options: 请求选项配置

        Returns:
            str: 文本内容
        """
        if options is None:
            options = RequestOptions()

        page = None
        try:
            page = await self.manager.new_page()
            await page.goto(url, wait_until=options.wait_for)

            if selector:
                element = await page.query_selector(selector)
                if element:
                    content = await element.text_content()
                    return content or ""
                return ""
            else:
                content = await page.text_content("body")
                return content or ""

        except Exception as e:
            logger.error(f"Extract text failed for {url}: {str(e)}")
            return ""
        finally:
            if page:
                await page.close()

    async def extract_links(self, url: str, selector: str = "a", options: Optional[RequestOptions] = None) -> List[str]:
        """
        提取页面链接

        Args:
            url: 请求URL
            selector: 链接选择器，默认为所有a标签
            options: 请求选项配置

        Returns:
            List[str]: 链接列表
        """
        if options is None:
            options = RequestOptions()

        page = None
        try:
            page = await self.manager.new_page()
            await page.goto(url, wait_until=options.wait_for)

            links = await page.evaluate(f"""
                Array.from(document.querySelectorAll('{selector}')).map(a => a.href)
            """)

            # 转换为绝对URL
            return [urljoin(url, link) for link in links if link]

        except Exception as e:
            logger.error(f"Extract links failed for {url}: {str(e)}")
            return []
        finally:
            if page:
                await page.close()

    async def wait_and_click(
        self, url: str, selector: str, options: Optional[RequestOptions] = None
    ) -> Tuple[str, int]:
        """
        等待元素出现并点击

        Args:
            url: 请求URL
            selector: 要点击的元素选择器
            options: 请求选项配置

        Returns:
            Tuple[str, int]: (页面内容, 状态码)
        """
        if options is None:
            options = RequestOptions()

        page = None
        try:
            page = await self.manager.new_page()
            response = await page.goto(url, wait_until=options.wait_for)
            if not response:
                raise Exception("Failed to load page")

            # 等待元素出现并点击
            await page.wait_for_selector(selector)
            await page.click(selector)

            # 等待页面响应
            await page.wait_for_load_state("networkidle")

            content = await page.content()
            return content, response.status

        except Exception as e:
            logger.error(f"Wait and click failed for {url}: {str(e)}")
            raise
        finally:
            if page:
                await page.close()

    async def close(self):
        """关闭浏览器"""
        await self.manager.stop()
