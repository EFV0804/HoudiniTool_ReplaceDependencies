# Houdini/Redshift
## Description
These scripts aim to make it easier to prepare hip files to be submitted to a farm, by remapping dependencies.
### houdini_replace_dependencies.py
This script prepares a houdini scene to be submitted to a farm as a Redshift proxy ( '.rs' file), by getting all dependencies paths, copying them to a specific location and remapping the dependencies of the hipfile. The aim is to bundle together the redshift proxy, the dependencies together in an easily movable and submitable package.
The pre_render() and post_render() can be called in Prism state manager before and after a .rs export for exemple.

### houdini_rs_override_textures.py
This script retrieves all Redshift texture paths and create a overrides.txt that can be used with the REDSHIFT_PATHOVERRIDE_FILE [environment variable](https://docs.redshift3d.com/display/RSDOCS/Intro+to+Proxies).

## Credits
- [MenhirFX](www.menhirfx.com)
