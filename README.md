# diagrams.net Libraries

## Create and share custom libraries:

1. Use the scratchpad or create a new library by clicking File, New Library
2. Once the library appears in the sidebar, you can drag and drop cells and images from the diagram or your harddrive
3. Supported image formats are PNG, JPG, SVG and GIF (including animated GIFs). If you are adding SVG files, you can make the colors of the SVG configurable using this method: https://www.drawio.com/doc/faq/svg-edit-colours
4. When all elements have been added, click the pen icon, add titles to the entries and click Export
5. This will download the library file to your computer
6. To share it, the file must be uploaded to the web and made available via a public URL. One way to do this is to upload it to a public GitHub repository.
7. If you are using GitHub, use the _RAW_ URL of the library which is of the form https://raw.githubusercontent.com/ORG/REPO/REF/PATH/FILENAME.xml, eg. https://raw.githubusercontent.com/jgraph/drawio-libs/main/libs/templates.xml
8. Once you have the URL of the library, you can share it by encoding the URL and adding it the clibs parameter. To encode the URL, paste it into the text box at https://jgraph.github.io/drawio-tools/tools/convert.html and click URL Encode. For our example, this will yield https%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ftemplates.xml
9. Then add this to https://app.diagrams.net/?splash=0&clibs=U, eg. https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ftemplates.xml (where splash=0 bypasses the splash screen). Multiple libraries can be specified by separating them with semicolons. Each value must be prefixed with a U if it's a URL, eg. https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fun-ocha-icons-bluebox.xml;Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fun-ocha-icons.xml
10. You can then share this link and clicking on it will open and install your custom libraries in draw.io

See also: https://www.drawio.com/blog/custom-libraries

## Library File Format

Libraries consist of an enclosing `<mxlibrary>` node containing a JSON array, which in turn contains entries with either an `xml` property with a compressed or uncompressed mxGraphModel or a `data` property with an image data URI (in PNG, JPG or SVG). All entries must have a `w` and `h` property for the width and height of the cell(s) or image in the entry and an optional `title` property for the title in the sidebar and preview. For entries with a `data` property, an optional `"aspect": "fixed"` may be specified to add `aspect=fixed` to the style of the image cell, and an optional `style` attribute can be specified to be added the default style of the image cell. Eg. for `"data": "data:image/png,[...]", "aspect": "fixed", "style": "resizable=0;rotatable=0;"` the resulting cell style will be `shape=image;verticalLabelPosition=bottom;verticalAlign=top;imageAspect=0;aspect=fixed;image=data:image/png,[...];resizable=0;rotatable=0;`

For uncompressed `xml` properties, `<` must be writter as `&lt;`, `>` must be written as `&gt;` and `"` must written as `\"` (escaped), eg. `"xml": "&lt;mxGraphModel&gt;&lt;root&gt;&lt;mxCell id=\"0\"/&gt;&lt;mxCell id=\"1\" parent=\"0\"/&gt;&lt;mxCell id=\"2\" value=\"Test3\" style=\"whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#000000;\" vertex=\"1\" parent=\"1\"&gt;&lt;mxGeometry width=\"120\" height=\"60\" as=\"geometry\"/&gt;&lt;/mxCell&gt;&lt;/root&gt;&lt;/mxGraphModel&gt;"`

The compressed XML may be obtained by clicking on the Encode button at https://jgraph.github.io/drawio-tools/tools/convert.html, eg. `"xml": "jVBLDoMgED3N7BE2XVdbV131BKROhASE4LTq7TsVWuPCpAuS95lH3gyo2s9t0tHcQocO1AVUnUKgjPxco3Mghe1ANSCl4AfyeuBWqyuiTjjQPwGZAy/tnpiVLIy0uCJwwMaRyXkylvAe9ePjTNyZNUOeSzcVw5D00GP5EBPhfFhqlUqjFoNHSguPTLYjkydOubcwaHtDe02Pmfe/5LYhg7Lkl27HXL3drd8="`

## Image (raster) Libraries

* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ftemplates.xml" target="_blank">Templates:</a> A sample library with basic building blocks for technical diagrams. The Comic template needs <a href="http://antiyawn.com/uploads/humorsans.html" target="_blank">Humor Sans</a>.
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fun-ocha-icons-bluebox.xml;Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fun-ocha-icons.xml" target="_blank">UN-OCHA Icons:</a> United Nations Office for the Coordination of Humanitarian Affairs (<a href="http://www.unocha.org" target="_blank">OCHA</a>) Humanitarian Icons 2012. Superseded by the UN-OCHA Icons v.02 vector library below.
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fraw.githubusercontent.com%2FLKirst%2Fgenogram%2Fmaster%2Fgenogram_library_lk.xml" target="_blank">Genogram:</a> A library with icons for genograms (also known as family diagrams).
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fdigitalocean.xml" target="_blank">DigitalOcean:</a> A library with icons for DigitalOcean resources (scraped from <https://do.co/diagram-kit> and <https://www.digitalocean.com/press>).
  * WARNING: No license is given by DO for these icons. Use at your own risk!

## Vector Libraries

* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fun-ocha-icons-v02.xml" target="_blank">UN-OCHA Icons v.02:</a> United Nations OCHA <a href="https://github.com/UN-OCHA/humanitarian-icons" target="_blank">Humanitarian Icons v.02</a> (CC0), 387 recolorable UN Blue icons. Successor to the 2012 raster set above.
  * NOTE: OCHA released a newer <a href="https://github.com/UN-OCHA/humanitarian-icons-2026-BDU" target="_blank">Humanitarian Icons 2026</a> set (389 icons, July 2026), but it is licensed CC BY 4.0; the v.02 set above remains the latest CC0 (public domain) release.
* <a href="https://app.diagrams.net/?libs=0&clibs=Uhttps%3A%2F%2Fraw.githubusercontent.com%2FCir02%2FApache-logos-drawio%2Fmain%2Flib%2Fapache_software_foundation_logos.xml" target="_blank">Apache Foundation logos:</a> The icon set by <a href="https://github.com/Cir02/Apache-logos-drawio" target="_blank">Cir02</a> of Apache foundation logos.
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fdelivery-icons.xml" target="_blank">Checkout & Delivery Icons:</a> The icon set by <a href="http://www.epicpxls.com/" target="_blank">EpicPxls</a> contains 35 icons depicting various actions and entities for the common checkout process on an e-commerce site.
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fosa-icons.xml" target="_blank">OSA Icons:</a> Open source free technical icons to create security architecture or other technical drawings <a href="http://www.opensecurityarchitecture.org/cms/library/icon-library" target="_blank">Open Security Architecture/</a>. (Classic colored set; see OSA Icons Mono below for the current monochrome library.)
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fosa-icons-mono.xml" target="_blank">OSA Icons (Mono):</a> Rebuilt <a href="https://opensecurityarchitecture.org/foundations/icons/" target="_blank">Open Security Architecture</a> icon library v2.6 — 79 monochrome stroke-based security icons with editable colours.
  * Icons © Open Security Architecture, licensed <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank">CC BY-SA 4.0</a>; repackaged for draw.io with editable-colour CSS classes, artwork otherwise unmodified.
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fflat-color-icons.xml" target="_blank">Flat Color Icons:</a> The complete set of 329 flat colour icons by <a href="https://github.com/icons8/flat-color-icons" target="_blank">Icons8</a>.
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fvoyage-icons.xml" target="_blank">Voyage Icons:</a> 40 free icons to spice up your travel agency or the airline website by <a href="http://www.printexpress.co.uk/" target="_blank">PrintExpress</a>.
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fgesture-icons.xml" target="_blank">Gesture and Fingerprints Icons:</a> 100 useful gesture and fingerprints line icons by <a href="http://thesquid.ink/flat-icons/" target="_blank">TheSquid</a>.
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fmaterial-design-icons.xml" target="_blank">Material Design Icons:</a> Material design icons are the official icon set from Google that are designed under the material design guidelines by <a href="https://design.google.com/icons/" target="_blank">Google</a>. (Classic set, frozen upstream since 2020 — see Material Symbols below.)
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fmaterial-symbols.xml" target="_blank">Material Symbols:</a> Google's current official icon set (3,894 icons, outlined style, recolorable), Apache 2.0 licensed, by <a href="https://fonts.google.com/icons" target="_blank">Google</a>.
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fchart-icons.xml" target="_blank">Chart Icons:</a> A set of light color chart icons.
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fwindows-10-icons.xml" target="_blank">Windows 10 Icons:</a> A set of Windows 10 icons.
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fgnome-icons.xml" target="_blank">Gnome Icons:</a> Network icons scheme based on Gnome Gorilla's theme.
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffont-awesome.xml" target="_blank">Font Awesome:</a> Font Awesome Free 7.3.1 solid and brand icons (1,994 icons, recolorable; Icons: CC BY 4.0) from <a href="https://fontawesome.com/" target="_blank">Font Awesome</a>.
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fhero-icons.xml" target="_blank">Heroicons:</a> 576 outline and solid icons (recolorable) by <a href="https://github.com/tailwindlabs/heroicons" target="_blank">Tailwind Labs</a> (MIT).
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Farista.xml" target="_blank">Arista Icons:</a> A set of Arista networking icons.
  * NOTE: Icons date from ~2016 (7010/7050/7150/7250/7280SE/7300/7500E families); the 7280R3/7500R3/7800R3 (2019) and 7060X6/7800R4/7700R4 Etherlink AI (2024) generations are missing. Current official Visio stencils are freely downloadable (no login) from the Literature section of any arista.com product page, but automated fetches are bot-blocked, so refreshing this library needs a manual download plus conversion.
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fcommvault%2Fcvlt-badges.xml;Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fcommvault%2Fcvlt-infrastructure.xml;Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fcommvault%2Fcvlt-objects.xml;Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fcommvault%2Fcvlt-protected-clients.xml" target="_blank">Commvault Icons:</a> A set of Commvault networking icons.
  * NOTE: These icons date from September 2019 and predate both Commvault's October 2019 logo change and the November 2023 "Commvault Cloud" rebrand. Commvault no longer publishes a public icon set (partner portal only), so this library cannot currently be refreshed.
* <a href="https://app.diagrams.net/?splash=0&clibs=
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Ffortinet-buildings.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Ffortinet-cloud.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Ffortinet-connector-devops_api.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Ffortinet-devices.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Ffortinet-features.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Ffortinet-generic-devices.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Ffortinet-generic-products.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Ffortinet-generic-technology.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Ffortinet-ot-and-iot.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Ffortinet-people-and-noc-soc.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Ffortinet-people-and-red-blue-team.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Ffortinet-platform-core-elements.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Ffortinet-products.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Ffortinet-saas-family-of-offerings.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Ffortinet-solutions-and-deployment-scenarios.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Ffortinet-threats-and-threat-services.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Ffortinet-vertical-related.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Ffortinet-vm-components.xml
" target="_blank">Fortinet Icons (2019):</a> A set of Fortinet networking icons from the September 2019 vendor library. Superseded by Fortinet Icons v2 below.
* <a href="https://app.diagrams.net/?splash=0&clibs=
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Fv2%2Flogos.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Fv2%2Fpillars.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Fv2%2Fform-factors.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Fv2%2Fsecure-networking.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Fv2%2Funified-sase.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Fv2%2Fsecurity-operations.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Fv2%2Fot-aware-security-fabric.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Fv2%2Ffortiguard-services.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffortinet%2Fv2%2Fdevices-and-verticals.xml
" target="_blank">Fortinet Icons v2 (2026):</a> The current official Fortinet icon library (<a href="https://icons.fortinet.com/" target="_blank">icons.fortinet.com</a>, June 2026), 796 icons in one library per group.
* <a href="https://app.diagrams.net/?splash=0&clibs=
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fintegration%2Fadditional-or-support.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fintegration%2Fai-machine-learning.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fintegration%2Fapps-and-system-logos.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fintegration%2Fazure.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fintegration%2Fazure-additional-or-support.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fintegration%2Fazure-integration-services.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fintegration%2Fbuildings.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fintegration%2Fdatabases.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fintegration%2Fdeprecated.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fintegration%2Fdeveloper.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fintegration%2Fdevices.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fintegration%2Ffiles.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fintegration%2Fgeneric.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fintegration%2Finfrastructure.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fintegration%2Fintegration.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fintegration%2Fintegration-patterns.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fintegration%2Fiot-devices.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fintegration%2Fmicrosoft-fabric.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fintegration%2Foffice365.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fintegration%2Fothers.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fintegration%2Fpowerapps-and-flows.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fintegration%2Fpower-bi.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fintegration%2Fsap.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fintegration%2Fservers.xml;
Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fintegration%2Fusers-and-roles.xml
" target="_blank">Integration Icons:</a> A set of MS Integration icons from <a href="https://github.com/sandroasp/Microsoft-Integration-and-Azure-Stencils-Pack-for-Visio" target="_blank">Sandro Pereira's stencil pack</a> (MIT), including the Microsoft Fabric and Azure Integration Services shapes added in pack v8.0.1.
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fmaki.xml" target="_blank">Maki Map Icons:</a> The complete set of 215 map/POI icons (recolorable) by <a href="https://github.com/mapbox/maki" target="_blank">Mapbox</a> (CC0), from v8.2.0 (July 2026).
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ftemaki.xml" target="_blank">Temaki Map Icons:</a> 557 map/POI icons (recolorable) extending the Maki set, by <a href="https://github.com/rapideditor/temaki" target="_blank">Temaki</a> (CC0), from v5.13.0 (July 2026).
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fnps%2Fnps-symbols.xml" target="_blank">NPS Symbols:</a> 294 recolorable wayfinding, recreation and accessibility pictographs from the US National Park Service <a href="https://github.com/nationalparkservice/symbol-library" target="_blank">symbol library</a> (BSD), snapshot 27e9720 (July 2026).
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ftabler%2Ftabler-outline.xml" target="_blank">Tabler Icons (Outline):</a> 5,112 recolorable outline icons by <a href="https://github.com/tabler/tabler-icons" target="_blank">Tabler</a> (MIT), v3.45.0 (July 2026).
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ftabler%2Ftabler-filled.xml" target="_blank">Tabler Icons (Filled):</a> 1,054 recolorable filled icons by <a href="https://github.com/tabler/tabler-icons" target="_blank">Tabler</a> (MIT), v3.45.0 (July 2026).
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffluent%2Ffluent-regular.xml" target="_blank">Fluent UI Icons (Regular):</a> Microsoft <a href="https://github.com/microsoft/fluentui-system-icons" target="_blank">Fluent UI System Icons</a> regular style, 2,904 recolorable icons (MIT), v1.1.333 (July 2026).
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffluent%2Ffluent-filled.xml" target="_blank">Fluent UI Icons (Filled):</a> Microsoft <a href="https://github.com/microsoft/fluentui-system-icons" target="_blank">Fluent UI System Icons</a> filled style, 2,943 recolorable icons (MIT), v1.1.333 (July 2026).
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fphosphor%2Fphosphor-regular.xml;Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fphosphor%2Fphosphor-fill.xml;Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fphosphor%2Fphosphor-duotone.xml" target="_blank">Phosphor Icons:</a> 1,512 icons per weight in Regular, Fill and Duotone (4,536 recolorable entries; duotone layer at 20% opacity) from <a href="https://phosphoricons.com/" target="_blank">Phosphor</a> (MIT), v2.1.1 (July 2026).
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Ffluent-emoji%2Ffluent-emoji.xml" target="_blank">Fluent Emoji (Flat):</a> Microsoft <a href="https://github.com/microsoft/fluentui-emoji" target="_blank">Fluent Emoji</a> in the Flat style — 1,595 emoji, default skin tone (MIT), snapshot July 2026.
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fcarbon%2Fcarbon-icons.xml" target="_blank">IBM Carbon Icons:</a> <a href="https://carbondesignsystem.com/elements/icons/library/" target="_blank">IBM Carbon Design System</a> icons — 2,715 recolorable icons including the Watson Health and quantum sets (Apache-2.0), @carbon/icons 11.84.0 (July 2026).
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fcarbon%2Fcarbon-pictograms.xml" target="_blank">IBM Carbon Pictograms:</a> <a href="https://carbondesignsystem.com/elements/pictograms/library/" target="_blank">IBM Carbon Design System</a> pictograms — 1,572 recolorable large-format pictograms (Apache-2.0), @carbon/pictograms 12.80.0 (July 2026).
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fhealth%2Fhealth-icons-outline.xml" target="_blank">Health Icons (Outline):</a> <a href="https://healthicons.org/" target="_blank">Health Icons</a> outline style — 741 recolorable public-health, medical and clinical icons (CC0), snapshot July 2026.
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fhealth%2Fhealth-icons-filled.xml" target="_blank">Health Icons (Filled):</a> <a href="https://healthicons.org/" target="_blank">Health Icons</a> filled style — 741 recolorable public-health, medical and clinical icons (CC0), snapshot July 2026.
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fflags%2Fflag-icons.xml" target="_blank">Country Flags:</a> All 271 country and region flags (4:3) from <a href="https://github.com/lipis/flag-icons" target="_blank">flag-icons</a> v7.5.0 (MIT), titled "Name (CODE)" (July 2026).
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fflags%2Fcircle-flags.xml" target="_blank">Circle Flags:</a> 444 circular flags — countries, subdivisions, language and other flags — from <a href="https://github.com/HatScripts/circle-flags" target="_blank">HatScripts/circle-flags</a> (MIT), snapshot July 2026.
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fgitlab%2Fgitlab-icons.xml" target="_blank">GitLab Icons:</a> GitLab's official UI icon set — 484 recolorable DevOps/CI icons (MIT) from <a href="https://gitlab.com/gitlab-org/gitlab-svgs" target="_blank">gitlab-org/gitlab-svgs</a> v3.163.0 (July 2026). GitLab logos (tanuki) and third-party file-type/brand logos are intentionally excluded.
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fmeteocons%2Fmeteocons.xml" target="_blank">Meteocons Weather:</a> 519 full-colour static weather icons (fill style) by <a href="https://github.com/basmilius/weather-icons" target="_blank">Bas Milius / Meteocons</a> (MIT), @meteocons/svg-static v0.1.0 (July 2026).
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fmeteocons%2Fmeteocons-line.xml" target="_blank">Meteocons Weather (Line):</a> 519 static weather icons in the line style (multicoloured) by <a href="https://github.com/basmilius/weather-icons" target="_blank">Bas Milius / Meteocons</a> (MIT), @meteocons/svg-static v0.1.0 (July 2026).
* <a href="https://app.diagrams.net/?splash=0&clibs=Uhttps%3A%2F%2Fjgraph.github.io%2Fdrawio-libs%2Flibs%2Fkubernetes.xml" target="_blank">Kubernetes Icons:</a> A set of Kubernetes icons. Obsolete, as there is currently an integrated set in the app.

Click on a link above to open a library or go to File, Open Library from URL in draw.io and enter an URL of the form https://jgraph.github.io/drawio-libs/libs/templates.xml
