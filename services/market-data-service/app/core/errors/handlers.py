import grpc
from app.domain.exceptions.exceptions import SymbolNotFoundException, TimeframeNotSupportedException

def handle_grpc_exception(context, exception):
    if isinstance(exception, SymbolNotFoundException):
        context.abort(
            grpc.StatusCode.NOT_FOUND,
            str(exception),
        )

    if isinstance(exception, TimeframeNotSupportedException):
        context.abort(
            grpc.StatusCode.INVALID_ARGUMENT,
            str(exception),
        )

    context.abort(
        grpc.StatusCode.INTERNAL,
        str(exception),
    )
