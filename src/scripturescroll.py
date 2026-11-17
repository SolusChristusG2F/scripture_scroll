import flet as ft
import pythonbible as bible
import random
from dataclasses import field

custom_group_dict = {
    "OLD_TESTAMENT" : bible.BookGroup.OLD_TESTAMENT,
    "OLD_TESTAMENT_LAW" : bible.BookGroup.OLD_TESTAMENT_LAW,
    "OLD_TESTAMENT_HISTORY" : bible.BookGroup.OLD_TESTAMENT_HISTORY,
    "OLD_TESTAMENT_POETRY_WISDOM" : bible.BookGroup.OLD_TESTAMENT_POETRY_WISDOM,
    "OLD_TESTAMENT_PROPHECY" : bible.BookGroup.OLD_TESTAMENT_PROPHECY,
    "OLD_TESTAMENT_MAJOR_PROPHETS" : bible.BookGroup.OLD_TESTAMENT_MAJOR_PROPHETS,
    "OLD_TESTAMENT_MINOR_PROPHETS" : bible.BookGroup.OLD_TESTAMENT_MINOR_PROPHETS,
    "NEW_TESTAMENT" : bible.BookGroup.NEW_TESTAMENT,
    "NEW_TESTAMENT_GOSPELS" : bible.BookGroup.NEW_TESTAMENT_GOSPELS,
    "NEW_TESTAMENT_HISTORY" : bible.BookGroup.NEW_TESTAMENT_HISTORY,
    "NEW_TESTAMENT_EPISTLES" : bible.BookGroup.NEW_TESTAMENT_EPISTLES,
    "NEW_TESTAMENT_PAUL_EPISTLES" : bible.BookGroup.NEW_TESTAMENT_PAUL_EPISTLES,
    "NEW_TESTAMENT_GENERAL_EPISTLES" : bible.BookGroup.NEW_TESTAMENT_GENERAL_EPISTLES,
    "NEW_TESTAMENT_APOCALYPTIC" : bible.BookGroup.NEW_TESTAMENT_APOCALYPTIC
}

class RandomVerse:
    #initialize necessary variables and generate the actual paramaters of the random verse itself
    def __init__(self, book_specific, group_specific, numerical_id=None, normalized_reference=None, book=None, group=None):
        self.numerical_id = numerical_id
        self.normalized_reference = normalized_reference
        self.book = book
        self.book_specific = book_specific
        self.group = group
        self.group_specific = group_specific
        self.generate()

    #generate the random verse, optionally from a specific book or group of books; can also be called repeatedly from the same instance to "reroll"
    def generate(self):
        if not self.book_specific:
            if not self.group_specific:
                book_number = random.randint(1, 66)
                self.book = bible.Book(book_number)
            else:
                book_number = random.randint(self.group.books[0].value, self.group.books[-1].value)
                self.book = bible.Book(book_number)
        else:
            book_number = self.book.value

        chapter_number = random.randint(1, bible.get_number_of_chapters(self.book))
        verse_number = random.randint(1, bible.get_number_of_verses(self.book, chapter_number))

        self.numerical_id = int(f"{book_number}" + str(chapter_number).zfill(3) + str(verse_number).zfill(3))
        self.normalized_reference = bible.convert_verse_ids_to_references([self.numerical_id])  

    def get_verse_text(self):
        return bible.get_verse_text(self.numerical_id)

    def get_plain_text_ref(self):
        return bible.format_scripture_references(self.normalized_reference)

@ft.control
class CenterColumn(ft.Column):
    def init(self):
        self.alignment="center"
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER

@ft.control
class CenterRow(ft.Row):
    def init(self):
        self.alignment = "center"
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER

@ft.control
class CenterScrollColumn(CenterColumn):
    def init(self):
        self.scroll = ft.ScrollMode.HIDDEN

@ft.control
class VerseRefText(ft.Text):
    color: ft.Colors = ft.Colors.GREY
    size: int = 35
    weight: ft.FontWeight = ft.FontWeight.BOLD
    overflow: ft.TextOverflow = ft.TextOverflow.FADE
    text_align: str = "center"

@ft.control
class VerseText(ft.Text):
    color: ft.Colors = ft.Colors.GREY
    size: int = 25
    overflow: ft.TextOverflow = ft.TextOverflow.FADE
    text_align: str = "center"

@ft.control
class VerseContainer(ft.Container):
    padding: int = 25
    width: int = 350
    height: int = 350
    border_radius: int = 30
    bgcolor: ft.Colors = ft.Colors.WHITE

@ft.control
class VersePage(CenterColumn): 
    def init(self):
        self.verse_text = VerseText(align=ft.Alignment.CENTER)
        self.verse_ref = VerseRefText(align=ft.Alignment.CENTER)
        self.bookmark_button = ft.IconButton(ft.Icons.BOOKMARK_ADD)
        self.alignment = ft.MainAxisAlignment.CENTER
        self.controls=[
            CenterRow(
                controls=[
                    VerseContainer(
                        content=CenterScrollColumn(
                            controls=[
                                self.verse_ref,
                                self.verse_text
                            ],
                        )
                    )
                ],
            ),
            CenterRow(
                controls=[
                    self.bookmark_button
                ]
            )
        ]
        

    def refresh(self, r_verse : RandomVerse, is_title=None, title=None, body=None):
        if not is_title:
            self.verse_text.value = r_verse.get_verse_text()
            self.verse_ref.value = r_verse.get_plain_text_ref()
        else:
            self.verse_text.value = body
            self.verse_ref.value = title

    def remove_bookmark_button(self):
        self.controls[1].controls.remove(self.bookmark_button)

@ft.control
class VerseContainer(ft.Container):
    padding: int = 25
    width: int = 350
    height: int = 350
    border_radius: int = 30
    bgcolor: ft.Colors = ft.Colors.WHITE

@ft.control
class BookmarkPage(CenterColumn): 
    def remove_self(e):
        e.parent.controls.remove(e)

    def init(self):
        self.verse_text = VerseText(align=ft.Alignment.CENTER)
        self.verse_ref = VerseRefText(align=ft.Alignment.CENTER)
        self.remove_button = ft.IconButton(ft.Icons.BOOKMARK_REMOVE)
        self.remove_button.on_click = self.remove_self
        self.alignment = ft.MainAxisAlignment.CENTER
        self.controls=[
            CenterRow(
                controls=[
                    VerseContainer(
                        content=CenterScrollColumn(
                            controls=[
                                self.verse_ref,
                                self.verse_text
                            ],
                        )
                    )
                ],
            ),
            CenterRow(
                controls=[
                    self.remove_button
                ]
            )
        ]
        

    def refresh(self, title=None, body=None):
        self.verse_text.value = body
        self.verse_ref.value = title   

@ft.control
class PoolDropdown(ft.Dropdown):
    options: list = field(
        default_factory=lambda:[
            ft.DropdownOption(key="entire", text="Entire Bible"),
            ft.DropdownOption(key="book", text="Book-specific"),
            ft.DropdownOption(key="group", text="Book Group-specific")
        ]
    )
    max_width: int = 220

@ft.control
class BookDropdown(ft.Dropdown):
    options: list = field(
        default_factory=lambda:[
            ft.DropdownOption(key="GENESIS", text="Genesis"),
            ft.DropdownOption(key="EXODUS", text="Exodus"),
            ft.DropdownOption(key="LEVITICUS", text="Leviticus"),
            ft.DropdownOption(key="NUMBERS", text="Numbers"),
            ft.DropdownOption(key="DEUTERONOMY", text="Deuteronomy"),
            ft.DropdownOption(key="JOSHUA", text="Joshua"),
            ft.DropdownOption(key="JUDGES", text="Judges"),
            ft.DropdownOption(key="RUTH", text="Ruth"),
            ft.DropdownOption(key="SAMUEL_1", text="1 Samuel"),
            ft.DropdownOption(key="SAMUEL_2", text="2 Samuel"),
            ft.DropdownOption(key="KINGS_1", text="1 Kings"),
            ft.DropdownOption(key="KINGS_2", text="2 Kings"),
            ft.DropdownOption(key="CHRONICLES_1", text="1 Chronicles"),
            ft.DropdownOption(key="CHRONICLES_2", text="2 Chronicles"),
            ft.DropdownOption(key="EZRA", text="Ezra"),
            ft.DropdownOption(key="NEHEMIAH", text="Nehemiah"),
            ft.DropdownOption(key="ESTHER", text="Esther"),
            ft.DropdownOption(key="JOB", text="Job"),
            ft.DropdownOption(key="PSALMS", text="Psalms"),
            ft.DropdownOption(key="PROVERBS", text="Proverbs"),
            ft.DropdownOption(key="ECCLESIASTES", text="Ecclesiastes"),
            ft.DropdownOption(key="SONG_OF_SONGS", text="Song of Songs"),
            ft.DropdownOption(key="ISAIAH", text="Isaiah"),
            ft.DropdownOption(key="JEREMIAH", text="Jeremiah"),
            ft.DropdownOption(key="LAMENTATIONS", text="Lamentations"),
            ft.DropdownOption(key="EZEKIEL", text="Ezekiel"),
            ft.DropdownOption(key="DANIEL", text="Daniel"),
            ft.DropdownOption(key="HOSEA", text="Hosea"),
            ft.DropdownOption(key="JOEL", text="Joel"),
            ft.DropdownOption(key="AMOS", text="Amos"),
            ft.DropdownOption(key="OBADIAH", text="Obadiah"),
            ft.DropdownOption(key="JONAH", text="Jonah"),
            ft.DropdownOption(key="MICAH", text="Micah"),
            ft.DropdownOption(key="NAHUM", text="Nahum"),
            ft.DropdownOption(key="HABAKKUK", text="Habakkuk"),
            ft.DropdownOption(key="ZEPHANIAH", text="Zephaniah"),
            ft.DropdownOption(key="HAGGAI", text="Haggai"),
            ft.DropdownOption(key="ZECHARIAH", text="Zechariah"),
            ft.DropdownOption(key="MALACHI", text="Malachi"),
            ft.DropdownOption(key="MATTHEW", text="Matthew"),
            ft.DropdownOption(key="MARK", text="Mark"),
            ft.DropdownOption(key="LUKE", text="Luke"),
            ft.DropdownOption(key="JOHN", text="John"),
            ft.DropdownOption(key="ACTS", text="Acts"),
            ft.DropdownOption(key="ROMANS", text="Romans"),
            ft.DropdownOption(key="CORINTHIANS_1", text="1 Corinthians"),
            ft.DropdownOption(key="CORINTHIANS_2", text="2 Corinthians"),
            ft.DropdownOption(key="GALATIANS", text="Galatians"),
            ft.DropdownOption(key="EPHESIANS", text="Ephesians"),
            ft.DropdownOption(key="PHILIPPIANS", text="Philippians"),
            ft.DropdownOption(key="COLOSSIANS", text="Colossians"),
            ft.DropdownOption(key="THESSALONIANS_1", text="1 Thessalonians"),
            ft.DropdownOption(key="THESSALONIANS_2", text="2 Thessalonians"),
            ft.DropdownOption(key="TIMOTHY_1", text="1 Timothy"),
            ft.DropdownOption(key="TIMOTHY_2", text="2 Timothy"),
            ft.DropdownOption(key="TITUS", text="Titus"),
            ft.DropdownOption(key="PHILEMON", text="Philemon"),
            ft.DropdownOption(key="HEBREWS", text="Hebrews"),
            ft.DropdownOption(key="JAMES", text="James"),
            ft.DropdownOption(key="PETER_1", text="1 Peter"),
            ft.DropdownOption(key="PETER_2", text="2 Peter"),
            ft.DropdownOption(key="JOHN_1", text="1 John"),
            ft.DropdownOption(key="JOHN_2", text="2 John"),
            ft.DropdownOption(key="JOHN_3", text="3 John"),
            ft.DropdownOption(key="JUDE", text="Jude"),
            ft.DropdownOption(key="REVELATION", text="Revelation"),
        ]
    )
    max_width: int = 220

@ft.control
class GroupDropdown(ft.Dropdown):
    options: list = field(
        default_factory=lambda:[
            ft.DropdownOption(key="OLD_TESTAMENT", text="Old Testament"),
            ft.DropdownOption(key="OLD_TESTAMENT_LAW", text="Law"),
            ft.DropdownOption(key="OLD_TESTAMENT_HISTORY", text="OT History"),
            ft.DropdownOption(key="OLD_TESTAMENT_POETRY_WISDOM", text="Wisdom and Poetry"),
            ft.DropdownOption(key="OLD_TESTAMENT_PROPHECY", text="Prophecy"),
            ft.DropdownOption(key="OLD_TESTAMENT_MAJOR_PROPHETS", text="Major Prophets"),
            ft.DropdownOption(key="OLD_TESTAMENT_MINOR_PROPHETS", text="Minor Prophets"),
            ft.DropdownOption(key="NEW_TESTAMENT", text="New Testament"),
            ft.DropdownOption(key="NEW_TESTAMENT_GOSPELS", text="Gospels"),
            ft.DropdownOption(key="NEW_TESTAMENT_HISTORY", text="NT History (Acts)"),
            ft.DropdownOption(key="NEW_TESTAMENT_EPISTLES", text="Epistles"),
            ft.DropdownOption(key="NEW_TESTAMENT_PAUL_EPISTLES", text="Pauline Epistles"),
            ft.DropdownOption(key="NEW_TESTAMENT_GENERAL_EPISTLES", text="General Epistles"),
            ft.DropdownOption(key="NEW_TESTAMENT_APOCALYPTIC", text="Apocalyptic (Revelation)")
        ]
    )
    max_width : int = 220
