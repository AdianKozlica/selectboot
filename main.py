#!/usr/bin/python3

from entries import efi_entries,grub_entries
from models import qjsonmodel
from sys import exit

from PyQt5.QtWidgets import (QApplication,QVBoxLayout,
                             QTabWidget,QWidget,
                             QPushButton,QTreeView,
                             QListWidget)

from PyQt5.QtCore import Qt,QModelIndex

import os
import sys
import subprocess

class MainWidget(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.efi_entries = efi_entries.get_entries()
        self.init_ui()

    def _get_full_path(self,index:QModelIndex):
        finding = True
        path = []

        while finding:
            parent = index.parent()
            path.append(index.data())

            if parent.data():
                index = parent
            else:
                finding = False

        path.reverse()

        return ">".join(path)
    
    def _grub_reboot(self,path:str):
        subprocess.call(["grub-reboot",path])
        subprocess.call(["reboot"])

    def _efi_reboot(self):
        selected_entry = self.efi_entry_list.currentIndex().data()
        boot_index = self.efi_entries.get(selected_entry)
        
        subprocess.call(["efibootmgr","-n",boot_index])
        subprocess.call(["reboot"])
    
    def reboot_clicked(self):
        index = self.tree.currentIndex()
        path = self._get_full_path(index)
        self._grub_reboot(path)

    def init_ui(self):
        main_layout = QVBoxLayout()
        
        boot_tab = QTabWidget()
        grub_widget = QWidget()
        efi_widget=  QWidget()

        grub_vbox = QVBoxLayout()
        grub_reboot_btn = QPushButton()
        
        self.tree = QTreeView()
        model = qjsonmodel.QJsonModel()
        entries = grub_entries.get_boot_entries()

        self.tree.setModel(model)
        self.tree.setColumnHidden(1,True)

        model.load(entries)
        model._headers = ("Boot Entry","")

        grub_reboot_btn.setText("Reboot")
        grub_reboot_btn.clicked.connect(self.reboot_clicked)

        grub_vbox.addWidget(grub_reboot_btn,alignment=Qt.AlignmentFlag.AlignLeft)
        grub_vbox.addWidget(self.tree)
        
        grub_widget.setLayout(grub_vbox)

        efi_vbox = QVBoxLayout()
        efi_reboot_btn = QPushButton()
        self.efi_entry_list = QListWidget()

        self.efi_entry_list.addItems(self.efi_entries.keys())
        
        efi_reboot_btn.setText("Reboot")
        efi_reboot_btn.clicked.connect(self._efi_reboot)

        efi_vbox.addWidget(efi_reboot_btn,alignment=Qt.AlignmentFlag.AlignLeft)
        efi_vbox.addWidget(self.efi_entry_list)
        efi_widget.setLayout(efi_vbox)

        boot_tab.addTab(grub_widget,"GRUB")
        boot_tab.addTab(efi_widget,"EFI")

        main_layout.addWidget(boot_tab)
        
        self.setFixedSize(450,350)
        self.setWindowTitle("Select Boot")
        self.setLayout(main_layout)

def main():
    app = QApplication([])
    
    main_widget = MainWidget()
    main_widget.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    if os.getuid() != 0:
        sys.stderr.write("Must be root!\n")
        exit()

    main()
