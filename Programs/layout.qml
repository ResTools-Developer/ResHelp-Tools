#HariOm
"""
Copyright 2024 Manav Amit Choudhary

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    visible: true
    width: 600
    height: 400
    title: "PubChem Database"
    color: "#F0F0F0"

    ColumnLayout {
        anchors.fill: parent
        spacing: 10
        padding: 20

        Label {
            text: "Select File:"
            font.pixelSize: 15
        }

        Button {
            text: "Select File"
            Layout.fillWidth: true
            onClicked: guiHandler.selectFile()
            style: ButtonStyle {
                background: Rectangle {
                    color: control.pressed ? "#E0E0E0" : "#F0F0F0"
                    border.color: "#909090"
                    border.width: 1
                    radius: 5
                }
            }
        }

        Label {
            text: "Selected File:"
            font.pixelSize: 15
        }

        TextEdit {
            id: selectedFileText
            readOnly: true
            Layout.fillWidth: true
            height: 50
            color: "#000000"
            background: "#FFFFFF"
        }

        Label {
            text: "Select Save Folder:"
            font.pixelSize: 15
        }

        Button {
            text: "Select Save Folder"
            Layout.fillWidth: true
            onClicked: guiHandler.selectSaveFolder()
            style: ButtonStyle {
                background: Rectangle {
                    color: control.pressed ? "#E0E0E0" : "#F0F0F0"
                    border.color: "#909090"
                    border.width: 1
                    radius: 5
                }
            }
        }

        Label {
            text: "Selected Save Folder:"
            font.pixelSize: 15
        }

        TextEdit {
            id: selectedSaveFolderText
            readOnly: true
            Layout.fillWidth: true
            height: 50
            color: "#000000"
            background: "#FFFFFF"
        }

        Label {
            text: "Select File Type:"
            font.pixelSize: 15
        }

        ComboBox {
            id: fileTypeComboBox
            model: ["sdf", "json", "xml", "asnt"]
            Layout.fillWidth: true
        }

        ProgressBar {
            id: progressBar
            visible: false
            Layout.fillWidth: true
        }

        Button {
            text: "Start Download"
            Layout.fillWidth: true
            onClicked: guiHandler.startDownload()
            style: ButtonStyle {
                background: Rectangle {
                    color: control.pressed ? "#E0E0E0" : "#F0F0F0"
                    border.color: "#909090"
                    border.width: 1
                    radius: 5
                }
            }
        }

        Button {
            text: "Retry Failed Downloads"
            Layout.fillWidth: true
            onClicked: guiHandler.retryFailedDownloads()
            style: ButtonStyle {
                background: Rectangle {
                    color: control.pressed ? "#E0E0E0" : "#F0F0F0"
                    border.color: "#909090"
                    border.width: 1
                    radius: 5
                }
            }
        }

        Label {
            text: "Status:"
            font.pixelSize: 15
        }

        TextEdit {
            id: statusText
            readOnly: true
            Layout.fillWidth: true
            height: 50
            color: "#000000"
            background: "#FFFFFF"
        }
    }
}
