import unittest
import data_analyze
from IRCHandler import get_names, get_channels

class DataAnalyzeNamesAndChannel(unittest.TestCase):
    def setUp(self):
        self.analyzer_channels = data_analyze.IRCDataAnalyzer(get_channels)
        self.analyzer_names = data_analyze.IRCDataAnalyzer(get_names)

    def test_channels_should_correct_line(self):
        self.analyzer_channels.add_raw_data(":irc.irc 322 erqwe: #Main\r\n")
        self.analyzer_channels.add_raw_data(":irc.irc 322 erqwe: #SubChan\r\n")
        self.assertEqual(["#Main", "#SubChan"], self.analyzer_channels.get_data())
        self.analyzer_channels.clear()

    def test_channels_incorrect_line(self):
        self.analyzer_channels.add_raw_data(":irc.irc 312 efewf: Eweqe qerq\r\n")
        self.analyzer_channels.add_raw_data("312 efewf: Eweqe qerq\r\n")
        self.analyzer_channels.add_raw_data("Hello world!\r\n")
        self.assertEqual([], self.analyzer_channels.get_data())
        self.analyzer_channels.clear()

    def test_names_correct_lines(self):
        self.analyzer_names.add_raw_data(":irc.irc 353 efewf:a B @z\r\n")
        self.analyzer_names.add_raw_data(":irc.irc 353 efewf:Y x @v\r\n")
        self.assertEqual(["@v", "@z", "a", "B", "x", "Y"],
                         self.analyzer_names.get_data())
        self.analyzer_names.clear()

    def test_names_incorrect_lines(self):
        self.analyzer_names.add_raw_data(":irc.irc 322 erqwe: #Main\r\n")
        self.analyzer_names.add_raw_data("Hello world!\r\n")
        self.analyzer_names.add_raw_data("dgsg sdfsdfw wreeeee dfsfsd")
        self.assertEqual([], self.analyzer_names.get_data())


