from decimal import Decimal
from requests import Response


def response_formatter(res: Response) -> str:
    method = res.request.method
    url = res.url
    status = res.status_code
    seconds = Decimal(str(res.elapsed.total_seconds())).quantize(Decimal('1.0'))
    size = Decimal(str(len(res.content) / float(1 << 10))).quantize(Decimal('1.0'))
    msg = f'{method} {url} [HTTP {status}, {seconds}s, {size}KB]'
    return msg
