from revolver_api.revolver_api.route import Router


# scan this directory and import all plugins
def scan_plugins():
    import importlib
    import pkgutil
    import plugins
    # print("scan_plugins",plugins)
    for importer, package_name, _ in pkgutil.iter_modules(plugins.__path__):
        # print("Found submodule %s (in %s)" % (module_name, package.__name__))
        # print("importer, package_name",importer, package_name)
        print("Find moudles:",package_name)
        # print("importlib.import_module",importlib.import_module)
        module = importlib.import_module(f"plugins.{package_name}")
        # print("module",module)
        if hasattr(module, "config"):
            # print("module.config",module.config)
            yield module.config
        else:
            print(f"module {package_name} has no config")
            
            

plugins = [{
    **c,
    "installed":True
} for c in scan_plugins() if c is not None]


def register_plugins(api:Router):
    # TODO:根据配置文件注册插件
    for plugin in plugins:
        if 'install' in plugin:
            plugin["install"](api)
        
