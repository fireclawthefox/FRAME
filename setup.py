import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="panda3d-frame",
    version="22.10",
    author="Fireclaw",
    author_email="fireclawthefox@gmail.com",
    description="A visual game editor for the Panda3D engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fireclawthefox/frame",
    packages=setuptools.find_packages(),
    include_package_data=True,
    #project_urls = {
    #    "Documentation": "https://github.com/fireclawthefox/FRAME/wiki"
    #},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Software Development :: User Interfaces",
    ],
    install_requires=[
        'panda3d~=1.10.11',
        'DirectFolderBrowser',
        'DirectGuiExtension~=22.09',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'panda3d-frame = panda3d_frame:main',
        ],
        'gui_scripts': [
            'panda3d-frame = panda3d_frame:main',
        ]
    }
)
