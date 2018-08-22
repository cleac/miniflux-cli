class AbstractContext:

    def view(self, screen):
        raise NotImplementedError


def elipsize(text: str, expect_width: int) -> str:
    if len(text) > expect_width:
        return text[:expect_width-3] + '...'
    if len(text) < expect_width:
        return text + ' ' * (expect_width - len(text))
    return text
