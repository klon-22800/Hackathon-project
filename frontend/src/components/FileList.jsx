import React, { useState } from "react";
import { List, Dropdown, Menu, Button, message, Modal, Input, Select } from "antd";
import { FolderOutlined, FileOutlined, EllipsisOutlined } from "@ant-design/icons";

const { Option } = Select;

const FileList = ({ files, currentPath, setCurrentPath, fetchFiles }) => {
    const [isShareModalVisible, setShareModalVisible] = useState(false);
    const [shareFolderPath, setShareFolderPath] = useState("");
    const [educationProgramm, setEducationProgramm] = useState("");
    const [course, setCourse] = useState(1);
    const [permission, setPermission] = useState(1);

    const handleDelete = (fileName) => {
        fetch(`http://localhost:8000/mydisk/files?path=${encodeURIComponent(currentPath)}&file_name=${encodeURIComponent(fileName)}`, {
            method: "DELETE",
            credentials: "include",
        })
            .then(() => {
                message.success("Файл успешно удалён!");
                fetchFiles();
            })
            .catch((error) => {
                console.error("Ошибка при удалении файла:", error);
                message.error("Не удалось удалить файл.");
            });
    };

    const handleDeleteFolder = async (folderPath) => {
        try {
            await fetch(`http://localhost:8000/mydisk/folders?path=${encodeURIComponent(folderPath)}`, {
                method: "DELETE",
                credentials: "include",
            });
            message.success("Папка успешно удалена!");
            fetchFiles();
        } catch (error) {
            console.error("Ошибка при удалении папки:", error);
            message.error("Не удалось удалить папку.");
        }
    };

    const handleShareFolder = async () => {
        try {
            const response = await fetch(`http://localhost:8000/mydisk/folders/share`, {
                method: "POST",
                credentials: "include",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    folder_path: shareFolderPath,
                    education_programm: educationProgramm,
                    course: course,
                    permission: permission,
                }),
            });

            if (response.ok) {
                message.success("Доступ успешно предоставлен!");
            } else {
                const errorData = await response.json();
                message.error(`Ошибка: ${errorData.detail || "Не удалось предоставить доступ"}`);
            }
        } catch (error) {
            console.error("Ошибка при предоставлении доступа:", error);
            message.error("Не удалось предоставить доступ.");
        } finally {
            setShareModalVisible(false);
            setEducationProgramm("");
            setCourse(1);
            setPermission(1);
            setShareFolderPath("");
        }
    };

    const showShareModal = (folderPath) => {
        setShareFolderPath(folderPath);
        setShareModalVisible(true);
    };

    const handleDownload = (fileName) => {
        fetch(`http://localhost:8000/mydisk/files/download?path=${encodeURIComponent(currentPath)}&file_name=${encodeURIComponent(fileName)}`, {
            method: "GET",
            credentials: "include",
        })
            .then((response) => response.blob())
            .then((blob) => {
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement("a");
                link.href = url;
                link.download = fileName;
                document.body.appendChild(link);
                link.click();
                link.remove();
            })
            .catch((error) => {
                console.error("Ошибка при скачивании файла:", error);
                message.error("Не удалось скачать файл.");
            });
    };

    const handleRename = (fileName) => {
        const newName = prompt(`Введите новое имя для ${fileName}`);
        if (newName) {
            fetch(`http://localhost:8000/mydisk/files/rename`, {
                method: "PUT",
                credentials: "include",
                body: JSON.stringify({ path: currentPath, old_name: fileName, new_name: newName }),
                headers: { "Content-Type": "application/json" },
            })
                .then(() => {
                    message.success("Файл успешно переименован!");
                    fetchFiles();
                })
                .catch((error) => {
                    console.error("Ошибка при переименовании файла:", error);
                    message.error("Не удалось переименовать файл.");
                });
        }
    };

    const navigateToFolder = (folderName) => {
        setCurrentPath(`${currentPath}${folderName}`);
    };

    const navigateBack = () => {
        const newPath = currentPath.split("/").slice(0, -2).join("/") + "/";
        const finalPath = newPath === "/" ? "" : newPath;
        setCurrentPath(finalPath || "");
    };

    return (
        <div>
            {currentPath && (
                <Button style={{ marginBottom: "10px" }} onClick={navigateBack}>
                    Назад
                </Button>
            )}
            <List
                bordered
                dataSource={files}
                renderItem={(fileName) => (
                    <List.Item
                        actions={[
                            <Dropdown
                                overlay={
                                    <Menu
                                        items={
                                            String(fileName).includes("/") // Проверяем, что это папка
                                                ? [
                                                    {
                                                        key: "delete-folder",
                                                        label: "Удалить папку",
                                                        onClick: () => handleDeleteFolder(`${currentPath}${fileName}`),
                                                    },
                                                    {
                                                        key: "share-folder",
                                                        label: "Поделиться",
                                                        onClick: () => showShareModal(`${currentPath}${fileName}`),
                                                    },
                                                ]
                                                : [
                                                    {
                                                        key: "delete-file",
                                                        label: "Удалить файл",
                                                        onClick: () => handleDelete(fileName),
                                                    },
                                                    {
                                                        key: "download",
                                                        label: "Скачать",
                                                        onClick: () => handleDownload(fileName),
                                                    },
                                                    {
                                                        key: "rename",
                                                        label: "Переименовать",
                                                        onClick: () => handleRename(fileName),
                                                    },
                                                ]
                                        }
                                    />
                                }
                                trigger={["click"]}
                            >
                                <Button
                                    type="text"
                                    icon={<EllipsisOutlined />}
                                    onClick={(e) => e.stopPropagation()} // Останавливаем всплытие события
                                />
                            </Dropdown>,
                        ]}
                        onClick={(e) => {
                            // Избегаем перехода внутрь папки, если кликнули на меню
                            if (e.target.closest("button")) return;

                            // Если это папка, позволяем переход
                            if (String(fileName).includes("/")) {
                                navigateToFolder(fileName);
                            }
                        }}
                    >
                        {String(fileName).includes("/") ? (
                            <FolderOutlined style={{ marginRight: "8px" }} />
                        ) : (
                            <FileOutlined style={{ marginRight: "8px" }} />
                        )}
                        {fileName}
                    </List.Item>

                )}
            />
            <Modal
                title="Поделиться папкой"
                visible={isShareModalVisible}
                onOk={handleShareFolder}
                onCancel={() => setShareModalVisible(false)}
                okText="Поделиться"
                cancelText="Отмена"
            >
                <Input
                    placeholder="Введите образовательную программу"
                    value={educationProgramm}
                    onChange={(e) => setEducationProgramm(e.target.value)}
                    style={{ marginBottom: "10px" }}
                />
                <Select
                    placeholder="Выберите курс"
                    value={course}
                    onChange={(value) => setCourse(value)}
                    style={{ width: "100%", marginBottom: "10px" }}
                >
                    <Option value={1}>Курс 1</Option>
                    <Option value={2}>Курс 2</Option>
                    <Option value={3}>Курс 3</Option>
                    <Option value={4}>Курс 4</Option>
                </Select>
                <Select
                    placeholder="Выберите уровень доступа"
                    value={permission}
                    onChange={(value) => setPermission(value)}
                    style={{ width: "100%" }}
                >
                    <Option value={1}>Только чтение</Option>
                    <Option value={2}>Чтение и запись</Option>
                </Select>
            </Modal>
        </div >
    );
};

export default FileList;