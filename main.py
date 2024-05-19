import flet as ft

def main(page: ft.Page) -> None:

    page.bgcolor = "#000000"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.fonts = {"appetite-italic": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf"}
    page.theme = ft.Theme(font_family="appetite-italic")

    score_text = ft.Text(value="", size=20, color="#ffb700")
    energy_text = ft.Text(value="", size=15, color="#00FFFF")

    score = 0
    energy = 50


    score_text.value = "{:.2f}".format(score)
    energy_text.value = f"Energy: {energy}"

    def handle_click(event: ft.ContainerTapEvent) -> None:
        nonlocal score_text, energy_text
        score = 0
        energy = 50

        if energy > 0:
            score += 0.02
            energy -= 1

            score_text.value = "{:.2f}".format(score)
            energy_text.value = f"Energy: {energy}"
            energy_progress_bar_fg.width = 250 * (energy / 50)

    def handle_ref_button(event: ft.TapEvent) -> None:
        pass

    def show_leaderboard(event: ft.TapEvent) -> None:
        pass


    leaderboard_button = ft.TextButton(text="Leaderboard", on_click=show_leaderboard)
    ref_button = ft.TextButton(text="Referral Link", on_click=handle_ref_button)

    buttons_row = ft.Row(controls=[leaderboard_button, ref_button], alignment=ft.MainAxisAlignment.CENTER)

    page.add(buttons_row)

    score = 0
    energy = 50

    energy_progress_bar_bg = ft.Container(
        height=10,
        width=250,
        bgcolor="#000000",
        margin=ft.Margin(top=30, right=0, left=15, bottom=-20)  # Сдвигаем влево на 50 пикселей
    )

    # Создание передней полосы прогресса для энергии
    energy_progress_bar_fg = ft.Container(
        height=10,
        width=250 * (energy / 50),
        bgcolor="#FFFF00",
        margin=ft.Margin(top=30, right=0, left=15, bottom=-20),  # Сдвигаем влево на 50 пикселей

    )

    progress_bar_stack = ft.Stack(controls=[energy_progress_bar_bg, energy_progress_bar_fg])

    # Clickable image
    clickable_image = ft.Image(src="cookies.png", fit=ft.ImageFit.CONTAIN, width=300, height=300)
    image_container = ft.Container(content=clickable_image, on_click=handle_click,
                                   margin=ft.Margin(top=50, right=0, left=0, bottom=0))
    page.add(image_container)

    # Создание контейнера для полос прогресса с ограничением максимальной ширины
    progress_bar_container = ft.Container(
        content=ft.Stack(controls=[energy_progress_bar_bg, energy_progress_bar_fg]),

        margin=ft.Margin(top=0, left=0, bottom=0, right=0),
        # Максимальная ширина контейнера

    )

    # Создание колонки для вертикального выравнивания элементов
    column = ft.Column(
        controls=[progress_bar_stack],
        expand=True,
    )

    # Размещение колонки на странице
    page.add(column)

    page.clickable_image = clickable_image
    page.energy_progress_bar_fg = energy_progress_bar_fg


if __name__ == "__main__":
    #ft.app(target=main, view=None, port=3001)
    ft.app(target=main, view=ft.WEB_BROWSER)
