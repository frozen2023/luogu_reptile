from problemReptile import *
from tkinter import *
from pathlib import Path
from pidReptile import *

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"../img")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def main():
    window = Tk()

    window.title("洛谷爬虫")
    window.geometry("1408x665")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=200,
        width=1408,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas_file = Canvas(
        window,
        bg="#D9D9D9",
        height=400,
        width=1408,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas_file.place(x=0, y=201)
    canvas.create_text(
        49.0,
        26.0,
        anchor="nw",
        text="所属题库",
        fill="#000000",
        font=("Inter", 24 * -1)
    )

    canvas.create_text(
        184.0,
        26.0,
        anchor="nw",
        text="洛谷",
        fill="#56B8E2",
        font=("Inter", 24 * -1)
    )

    canvas.create_text(
        42.0,
        87.0,
        anchor="nw",
        text="筛选条件",
        fill="#000000",
        font=("Inter", 24 * -1)
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        308.0,
        101.5,
        image=entry_image_1
    )
    difficulty = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    difficulty.place(
        x=234.0,
        y=86.0,
        width=148.0,
        height=29.0
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        623.0,
        103.0,
        image=entry_image_2
    )
    tag = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    tag.place(
        x=509.0,
        y=87.0,
        width=228.0,
        height=30.0
    )

    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(
        973.5,
        101.0,
        image=entry_image_3
    )
    keyword = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    keyword.place(
        x=858.0,
        y=85.0,
        width=231.0,
        height=30.0
    )

    canvas.create_text(
        162.0,
        86.0,
        anchor="nw",
        text="难度",
        fill="#000000",
        font=("Inter", 24 * -1)
    )

    canvas.create_text(
        434.0,
        85.0,
        anchor="nw",
        text="算法",
        fill="#000000",
        font=("Inter", 24 * -1)
    )

    canvas.create_text(
        776.0,
        86.0,
        anchor="nw",
        text="关键词",
        fill="#000000",
        font=("Inter", 24 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: invoke(),
        relief="flat"
    )
    button_1.place(
        x=1165.0,
        y=86.0,
        width=96.0,
        height=33.0
    )
    window.resizable(False, False)

    totalLog = 16
    baseX = 42
    baseY = 30
    space = 20
    logText = ""
    countText = ""
    endText = ""
    logFill = "#000000"
    countFill = "green"
    endFill = "blue"
    logFont = ("Inter", 17 * -1)
    countFont = ("Inter", 20 * -1)
    endFont = ("Inter", 20 * -1)

    logs = []

    countLog = canvas_file.create_text(
        baseX,
        0,
        anchor="nw",
        text=countText,
        fill=countFill,
        font=countFont
    )

    for i in range(totalLog):
        log = canvas_file.create_text(
            baseX,
            baseY + space * i,
            anchor="nw",
            text=logText,
            fill=logFill,
            font=logFont
        )

        logs.append(log)
    print("初始化了{}条日志".format(totalLog))

    endLog = canvas_file.create_text(
        baseX,
        baseY + space * totalLog,
        anchor="nw",
        text=endText,
        fill=endFill,
        font=endFont
    )

    # 爬取逻辑
    def invoke():

        # 根据输入的条件爬取pid
        totalCount, problems = getPids(difficulty.get(), tag.get(), keyword.get())

        # 计算爬取的数目，最多前50题
        cnt = 0
        for item in problems:
            pid = item["pid"]
            title = item["title"]
            getProblem(pid, title)
            cnt += 1
            if cnt == 50:
                break

    window.mainloop()


if __name__ == '__main__':
    main()
