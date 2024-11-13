import pkgutil
import os
import pkg_resources

def check_and_install_specific_version(package_name, version):
    package_version = f"{package_name}=={version}"
    try:
        pkg_resources.require(package_version)
    except pkg_resources.VersionConflict:
        print(f"Atualizando {package_name} para a versão {version}...")
        os.system(f"pip install --upgrade {package_version} --user")
    except pkg_resources.DistributionNotFound:
        print(f"Instalando {package_name} na versão {version}...")
        os.system(f"pip install {package_version} --user")
        
installed_packages = pkg_resources.working_set
installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
list_libraries_install = [i.split('==')[0] for i in installed_packages_list]     

libraries = [
    "smtplib", "requests", "json", "time", "re", "beautifulsoup4", "lxml", "email-validator"
]

check_and_install_specific_version("pandas", "2.2.1")
check_and_install_specific_version("openpyxl", "3.1.0")

for library_name in libraries:
    library_name_formatted = library_name.replace('_', '-').lower()
    if library_name_formatted not in list_libraries_install and pkgutil.find_loader(library_name_formatted) is None:
        print(f'Instalando biblioteca: {library_name_formatted}...')
        os.system(f"pip install {library_name_formatted} --user")