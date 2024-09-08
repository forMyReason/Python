# HEADER   :
#   File     :   python_menu.py
#   Create   :   2024/09/09
#   Author   :   LiDanyang 
#   Branch   :   develop
#   Descript :   添加一个菜单项

# Reference  :
#   1. https://www.jianshu.com/p/1abf4d85105e

import unreal

def main():
    print("Creating Menus!")
    menus = unreal.ToolMenus.get()
    main_menu = menus.find_menu("LevelEditor.MainMenu")
    if not main_menu:
        print("Failed to find the 'Main' menu. Something is wrong in the force!")

    entry = unreal.ToolMenuEntry(
        name="Python.Tools",
        type=unreal.MultiBlockType.MENU_ENTRY,
        insert_position=unreal.ToolMenuInsert("", unreal.ToolMenuInsertType.FIRST)
    )
    entry.set_label("Test")
    entry.set_string_command(unreal.ToolMenuStringCommandType.PYTHON, "Name", "print('这是一个测试')")
    script_menu = main_menu.add_sub_menu(main_menu.get_name(), "TestTools", "TestTools", "TestTools")
    script_menu.add_menu_entry("Scripts", entry)
    menus.refresh_all_widgets()


if __name__ == '__main__':
    main()