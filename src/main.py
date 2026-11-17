import flet as ft
from scripturescroll import *

def main(page: ft.Page):
    page.title = "Scripture Scroll"
    page.bgcolor = ft.Colors.BLUE_GREY
    page.appbar = ft.AppBar(bgcolor=ft.Colors.BLUE_GREY_400, title=ft.Text("Scripture Scroll", text_align="center", align=ft.Alignment.CENTER))

    verse = RandomVerse(book_specific=False, group_specific=False)
    verse_page = VersePage()

    def add_bookmark(e):
        ref = e.control.parent.parent.verse_ref.value
        verse = e.control.parent.parent.verse_text.value
        bookmark_page = VersePage()
        bookmark_page.refresh(verse, True, ref, verse)
        bookmark_page.remove_bookmark_button()

        if not bookmark_page in bookmarks_view.controls:
            bookmarks_view.controls.append(bookmark_page)

    def new_verse(e):
            verse.generate()
            verse_page = VersePage()
            verse_page.refresh(verse)
            verse_page.bookmark_button.on_click=add_bookmark
            
            main_view.controls.append(
                verse_page
            )

    first_page = VersePage()
    first_page.refresh(verse, True, "Scripture Scroll", "Welcome to Scripture Scroll! Swipe up to get started!")
    first_page.remove_bookmark_button()

    second_page = VersePage()
    second_page.refresh(verse)
    second_page.bookmark_button.on_click=add_bookmark

    main_view = ft.PageView(
        on_change=new_verse,
        horizontal=False,
        expand=True,
        controls=[
            first_page,
            second_page
        ]
    )

    def refresh_last():
        verse.generate()
        verse_page.refresh(verse)
        main_view.controls[-1] = verse_page

    def book_selected(e):
        verse.book = bible.get_references(book_dropdown.text)[0].book
        refresh_last()

    def group_selected(e):
        verse.group = custom_group_dict[group_dropdown.value]
        refresh_last()

    book_dropdown = BookDropdown(value="JOHN", on_select=book_selected)
    group_dropdown = GroupDropdown(value="NEW_TESTAMENT_GOSPELS", on_select=group_selected)

    def pool_changed(e):
        if e.control.value == "entire":
            verse.book_specific = False
            verse.group_specific = False

            if book_dropdown in e.control.parent.controls:
                e.control.parent.controls.remove(book_dropdown)

            if group_dropdown in e.control.parent.controls:
                e.control.parent.controls.remove(group_dropdown)

            refresh_last()
        elif e.control.value == "book":
            verse.book_specific = True
            verse.group_specific = False
            verse.book = bible.Book.JOHN
            e.control.parent.controls.append(book_dropdown)

            if group_dropdown in e.control.parent.controls:
                e.control.parent.controls.remove(group_dropdown)

            refresh_last()
        else:
            verse.book_specific = False
            verse.group_specific = True
            verse.group = bible.BookGroup.OLD_TESTAMENT_POETRY_WISDOM
            e.control.parent.controls.append(group_dropdown)

            if book_dropdown in e.control.parent.controls:
                e.control.parent.controls.remove(book_dropdown)

            refresh_last()

    settings_view = CenterScrollColumn(
        controls=[
            VerseText("Verse pool:", color=ft.Colors.WHITE),
            PoolDropdown(value="entire", on_select=pool_changed)
        ]
    )

    bookmark_start = VersePage()
    bookmark_start.refresh(verse, is_title=True, title="Bookmarks", body="Find all your bookmars here! Simply click the button on the bottom of any verse to bookmark it!")
    bookmark_start.remove_bookmark_button()

    bookmarks_view = ft.PageView(
        horizontal=False,
        expand=True,
        controls=[
            bookmark_start
        ]
    )

    def return_to_main(e):
        if not main_view in page.controls:
            page.clean()
            page.add(main_view)

    def switch_to_settings(e):
        if not settings_view in page.controls:
            page.clean()
            page.add(settings_view)

    def switch_to_bookmarks(e):
        if not bookmarks_view in page.controls:
            page.clean()
            page.add(bookmarks_view)

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.IconButton(ft.Icons.SWIPE_UP, on_click=return_to_main),
            ft.IconButton(ft.Icons.BOOK, on_click=switch_to_bookmarks),
            ft.IconButton(ft.Icons.SETTINGS, on_click=switch_to_settings)
        ]
    )
    
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(
        main_view
    )

if __name__ == "__main__":
    ft.run(main)
