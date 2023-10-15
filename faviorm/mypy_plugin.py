from typing import Callable

from mypy.plugin import FunctionContext, Plugin
from mypy.types import TupleType, Type


def hook(context: FunctionContext) -> Type:
    return TupleType(
        items=list(
            map(lambda c: c.args[0], context.arg_types[0])  # type: ignore
        ),
        fallback=context.api.named_generic_type("builtins.tuple", []),
        line=context.default_return_type.line,
        column=context.default_return_type.column,
    )


class FaviormPlugin(Plugin):
    def get_function_hook(
        self, fullname: str
    ) -> Callable[[FunctionContext], Type] | None:
        if fullname == "faviorm.sql.select.select":
            return hook
        return None


def plugin(version: str) -> type[FaviormPlugin]:
    return FaviormPlugin
