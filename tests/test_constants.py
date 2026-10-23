"""
tests for the downloader file
"""
import os
import tempfile
import unittest
import mock


from wahoomc.constants_functions import translate_tags_to_keep, \
    get_tag_wahoo_xml_path, TagWahooXmlNotFoundError, \
    get_map_writer_plugin_dirs, get_map_writer_plugin_path
from wahoomc.constants import RESOURCES_DIR, USER_DIR, MAP_WRITER_PLUGIN_FILENAME


tags_universal_simple = {"TAGS_TO_KEEP_UNIVERSAL": {
    'access': '',
    'area': 'yes'
}}

tags_universal_adv = {"TAGS_TO_KEEP_UNIVERSAL": {
    'access': '',
    'area': 'yes',
    'bicycle': '',
    'bridge': '',
    'foot': ['ft_yes', 'foot_designated']
}}


class TestTranslateTags(unittest.TestCase):
    """
    tests for translating tags-constants between the universal format and OS-specific formats
    """

    @ mock.patch("wahoomc.file_directory_functions.json.load")
    @ mock.patch("wahoomc.open")
    def test_translate_tags_to_keep_simple_macos(self, mock_open, mock_json_load):  # pylint: disable=unused-argument
        """
        Test translating tags to keep from universal format to macOS
        """
        tags = ['access', 'area=yes']
        mock_json_load.return_value = tags_universal_simple

        transl_tags = translate_tags_to_keep()
        self.assertEqual(tags, transl_tags)

    @ mock.patch("wahoomc.file_directory_functions.json.load")
    @ mock.patch("wahoomc.open")
    def test_translate_tags_to_keep_simple_win(self, mock_open, mock_json_load):  # pylint: disable=unused-argument
        """
        Test translating tags to keep from universal format to Windows
        """
        tags_win = 'access= area=yes'
        mock_json_load.return_value = tags_universal_simple

        transl_tags = translate_tags_to_keep(sys_platform='Windows')
        self.assertEqual(tags_win, transl_tags)

    @ mock.patch("wahoomc.file_directory_functions.json.load")
    @ mock.patch("wahoomc.open")
    def test_translate_tags_to_keep_adv_macos(self, mock_open, mock_json_load):  # pylint: disable=unused-argument
        """
        Test translating tags to keep from universal format to macOS
        """
        tags = ['access', 'area=yes', 'bicycle',
                'bridge', 'foot=ft_yes, foot_designated']
        mock_json_load.return_value = tags_universal_adv

        transl_tags = translate_tags_to_keep()
        self.assertEqual(tags, transl_tags)

    @ mock.patch("wahoomc.file_directory_functions.json.load")
    @ mock.patch("wahoomc.open")
    def test_translate_tags_to_keep_adv_win(self, mock_open, mock_json_load):  # pylint: disable=unused-argument
        """
        Test translating tags to keep from universal format to Windows
        """
        tags_win = 'access= area=yes bicycle= bridge= foot=ft_yes =foot_designated'
        mock_json_load.return_value = tags_universal_adv

        transl_tags = translate_tags_to_keep(sys_platform='Windows')
        self.assertEqual(tags_win, transl_tags)

    def test_translate_tags_to_keep_full_macos(self):
        """
        Test translating tags to keep from universal format to macOS // all "tags to keep"
        """
        tags = ['access', 'area=yes', 'bicycle', 'bridge', 'foot=ft_yes, foot_designated',
                'amenity=fuel, cafe, drinking_water, shelter', 'shop=bakery, bicycle',
                'highway=abandoned, bus_guideway, disused, bridleway, byway, construction, cycleway, footway, living_street, motorway, motorway_link, path, pedestrian, primary, primary_link, residential, road, secondary, secondary_link, service, steps, tertiary, tertiary_link, track, trunk, trunk_link, unclassified',
                'natural=coastline, nosea, sea, beach, land, scrub, water, wetland, wood',
                'landuse=forest, commercial, industrial, residential, retail',
                'leisure=park, nature_reserve', 'railway=rail, tram, station, stop',
                'surface', 'tracktype', 'tunnel', 'waterway=canal, drain, river, riverbank, stream', 'wood=deciduous', 'tourism=alpine_hut']

        transl_tags = translate_tags_to_keep(use_repo=True)
        self.assertEqual(tags, transl_tags)

    def test_translate_tags_to_keep_full_win(self):
        """
        Test translating tags to keep from universal format to Windows // all "tags to keep"
        """
        tags_win = 'access= area=yes bicycle= bridge= foot=ft_yes =foot_designated amenity=fuel =cafe =drinking_water =shelter shop=bakery =bicycle highway=abandoned =bus_guideway =disused =bridleway =byway =construction =cycleway =footway =living_street =motorway =motorway_link =path =pedestrian =primary =primary_link =residential =road =secondary =secondary_link =service =steps =tertiary =tertiary_link =track =trunk =trunk_link =unclassified natural=coastline =nosea =sea =beach =land =scrub =water =wetland =wood landuse=forest =commercial =industrial =residential =retail leisure=park =nature_reserve railway=rail =tram =station =stop surface= tracktype= tunnel= waterway=canal =drain =river =riverbank =stream wood=deciduous tourism=alpine_hut'

        transl_tags = translate_tags_to_keep(
            sys_platform='Windows', use_repo=True)
        self.assertEqual(tags_win, transl_tags)

    def test_translate_name_tags_to_keep_full_macos(self):
        """
        Test translating name tags to keep from universal format to Windows // all "name tags to keep"
        """
        names_tags = ['admin_level=2', 'area=yes', 'mountain_pass', 'natural',
                      'place=city, hamlet, island, isolated_dwelling, islet, locality, suburb, town, village, country']

        transl_tags = translate_tags_to_keep(name_tags=True, use_repo=True)
        self.assertEqual(names_tags, transl_tags)

    def test_translate_name_tags_to_keep_full_win(self):
        """
        Test translating name tags to keep from universal format to macOS // all "name tags to keep"
        """

        names_tags_win = 'admin_level=2 area=yes mountain_pass= natural= place=city =hamlet =island =isolated_dwelling =islet =locality =suburb =town =village =country'

        transl_tags = translate_tags_to_keep(
            name_tags=True, sys_platform='Windows', use_repo=True)
        self.assertEqual(names_tags_win, transl_tags)


class TestMapWriterPluginSearchPath(unittest.TestCase):
    """
    tests for the search path of the Osmosis mapwriter plugin
    """

    def test_dirs_default_order(self):
        """
        the system-wide location takes precedence over the user location
        """
        with mock.patch.dict(os.environ, {}, clear=True):
            plugin_dirs = get_map_writer_plugin_dirs()

        self.assertEqual('/usr/share/osmosis', plugin_dirs[0])
        self.assertEqual(
            os.path.join(USER_DIR, '.openstreetmap', 'osmosis', 'plugins'),
            plugin_dirs[-1])

    def test_dirs_override_first(self):
        """
        WAHOOMC_OSMOSIS_PLUGIN_DIR is searched first
        """
        with mock.patch.dict(os.environ, {'WAHOOMC_OSMOSIS_PLUGIN_DIR': '/opt/osmosis'}, clear=True):
            plugin_dirs = get_map_writer_plugin_dirs()

        self.assertEqual('/opt/osmosis', plugin_dirs[0])

    def test_path_prefers_existing_plugin(self):
        """
        an existing plugin is returned even if it is not the highest precedence dir
        """
        with tempfile.TemporaryDirectory() as plugin_dir:
            expected = os.path.join(
                plugin_dir, MAP_WRITER_PLUGIN_FILENAME)
            with open(expected, 'w', encoding='utf-8'):
                pass

            with mock.patch.dict(os.environ, {'WAHOOMC_OSMOSIS_PLUGIN_DIR': plugin_dir}, clear=True):
                self.assertEqual(expected, get_map_writer_plugin_path())

    def test_path_falls_back_to_user_dir(self):
        """
        without an existing plugin the user directory is the download target
        """
        with mock.patch.dict(os.environ, {'WAHOOMC_OSMOSIS_PLUGIN_DIR': '/nonexistent'}, clear=True):
            self.assertEqual(
                os.path.join(USER_DIR, '.openstreetmap', 'osmosis', 'plugins',
                             MAP_WRITER_PLUGIN_FILENAME),
                get_map_writer_plugin_path())


class TestTagWahooXML(unittest.TestCase):
    """
    tests for tag-wahoo xml file
    """

    def test_not_existing_tag_wahoo_xml(self):
        """
        check if a non-existing tag-wahoo xml file issues an exception
        """
        with self.assertRaises(TagWahooXmlNotFoundError):
            get_tag_wahoo_xml_path("not_existing.xml")

    def test_existing_tag_wahoo_xml(self):
        """
        check if the correct path of an existing tag-wahoo xml file is returned
        """

        expected_path = os.path.join(
            RESOURCES_DIR, "tag_wahoo_adjusted", "tag-wahoo-poi.xml")
        self.assertEqual(get_tag_wahoo_xml_path(
            "tag-wahoo-poi.xml"), expected_path)


if __name__ == '__main__':
    unittest.main()
