"""
Declaration of `Configuration` class.
"""

from copy import deepcopy
from typing import Optional, get_type_hints

_INSECURE_KEY_CACHE_LOCATION: Optional[str] = None


class Configuration:
    """
    Configuration class, to allow the compilation process to be customized.
    """

    # pylint: disable=too-many-instance-attributes

    verbose: bool
    show_graph: bool
    show_mlir: bool
    dump_artifacts_on_unexpected_failures: bool
    enable_unsafe_features: bool
    virtual: bool
    use_insecure_key_cache: bool
    loop_parallelize: bool
    dataflow_parallelize: bool
    auto_parallelize: bool
    jit: bool

    # pylint: enable=too-many-instance-attributes

    def _validate(self):
        """
        Validate configuration.
        """

        if not self.enable_unsafe_features:

            if self.use_insecure_key_cache:
                raise RuntimeError(
                    "Insecure key cache cannot be used without enabling unsafe features"
                )

            if self.virtual:
                raise RuntimeError(
                    "Virtual compilation is not allowed without enabling unsafe features"
                )

    # pylint: disable=too-many-arguments

    def __init__(
        self,
        verbose: bool = False,
        show_graph: bool = False,
        show_mlir: bool = False,
        dump_artifacts_on_unexpected_failures: bool = True,
        enable_unsafe_features: bool = False,
        virtual: bool = False,
        use_insecure_key_cache: bool = False,
        loop_parallelize: bool = True,
        dataflow_parallelize: bool = False,
        auto_parallelize: bool = False,
        jit: bool = False,
    ):
        self.verbose = verbose
        self.show_graph = show_graph
        self.show_mlir = show_mlir
        self.dump_artifacts_on_unexpected_failures = dump_artifacts_on_unexpected_failures
        self.enable_unsafe_features = enable_unsafe_features
        self.virtual = virtual
        self.use_insecure_key_cache = use_insecure_key_cache
        self.loop_parallelize = loop_parallelize
        self.dataflow_parallelize = dataflow_parallelize
        self.auto_parallelize = auto_parallelize
        self.jit = jit

        self._validate()

    # pylint: enable=too-many-arguments

    @staticmethod
    def insecure_key_cache_location() -> Optional[str]:
        """
        Get insecure key cache location.

        Returns:
            Optional[str]:
                insecure key cache location if configured, None otherwise
        """

        return _INSECURE_KEY_CACHE_LOCATION

    def fork(self, **kwargs) -> "Configuration":
        """
        Get a new configuration from another one specified changes.

        Args:
            **kwargs:
                changes to make

        Returns:
            Configuration:
                configuration that is forked from self and updated using kwargs
        """

        result = deepcopy(self)

        hints = get_type_hints(Configuration)
        for name, value in kwargs.items():
            if name not in hints:
                raise TypeError(f"Unexpected keyword argument '{name}'")

            hint = hints[name]
            if not isinstance(value, hint):  # type: ignore
                raise TypeError(
                    f"Unexpected type for keyword argument '{name}' "
                    f"(expected '{hint.__name__}', got '{type(value).__name__}')"
                )

            setattr(result, name, value)

        # pylint: disable=protected-access
        result._validate()
        # pylint: enable=protected-access

        return result