import React, { useState } from "react";
import { Form, Input, Button, message, Select } from "antd";
import { useNavigate } from "react-router-dom";

const { Option } = Select;

const RegistrationForm = () => {
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    // Состояние для полей формы
    const [formData, setFormData] = useState({
        name: "",
        email: "",
        password: "",
        role: "",
        education_programm: "",
        course: 1
    });

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSelectChange = (name, value) => {
        setFormData({
            ...formData,
            [name]: value,
        });
    };

    const handleSubmit = async () => {
        setLoading(true);
        try {
            // Если роль — учитель, устанавливаем значения по умолчанию
            const dataToSend = {
                ...formData,
                education_programm: formData.role === 2 ? "N/A" : formData.education_programm,
                course: formData.role === 2 ? 1 : parseInt(formData.course),
            };

            const response = await fetch("http://localhost:8000/auth/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(dataToSend),
            });

            if (response.ok) {
                message.success("Вы успешно зарегистрированы!");
                navigate("/login");
            } else {
                message.error("Ошибка при регистрации!");
            }
        } catch (error) {
            message.error("Ошибка при регистрации!");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ maxWidth: "400px", margin: "0 auto" }}>
            <Form onFinish={handleSubmit}>
                <Form.Item
                    label="Имя"
                    name="name"
                    rules={[{ required: true, message: "Пожалуйста, введите имя" }]}
                >
                    <Input
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                        placeholder="Введите имя"
                    />
                </Form.Item>

                <Form.Item
                    label="Email"
                    name="email"
                    rules={[{ required: true, message: "Пожалуйста, введите email" }]}
                >
                    <Input
                        name="email"
                        type="email"
                        value={formData.email}
                        onChange={handleChange}
                        placeholder="Введите email"
                    />
                </Form.Item>

                <Form.Item
                    label="Пароль"
                    name="password"
                    rules={[{ required: true, message: "Пожалуйста, введите пароль" }]}
                >
                    <Input.Password
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        placeholder="Введите пароль"
                    />
                </Form.Item>

                <Form.Item
                    label="Роль"
                    name="role"
                    rules={[{ required: true, message: "Пожалуйста, выберите роль!" }]}
                >
                    <Select
                        placeholder="Выберите роль"
                        onChange={(value) => handleSelectChange("role", value)}
                        value={formData.role}
                    >
                        <Option value={1}>Студент</Option>
                        <Option value={2}>Преподаватель</Option>
                    </Select>
                </Form.Item>

                {formData.role === 1 && (
                    <>
                        <Form.Item
                            label="Образовательная программа"
                            name="education_programm"
                            rules={[{ required: true, message: "Пожалуйста, выберите образовательную программу!" }]}
                        >
                            <Select
                                placeholder="Выберите программу"
                                onChange={(value) => handleSelectChange("education_programm", value)}
                                value={formData.education_programm}
                            >
                                <Option value="ИБАС">ИБАС</Option>
                                <Option value="ИВТ">ИВТ</Option>
                                <Option value="ПМИ">ПМИ</Option>
                                <Option value="ПМФ">ПМФ</Option>
                                <Option value="ФИИТ">ФИИТ</Option>
                            </Select>
                        </Form.Item>

                        <Form.Item
                            label="Курс"
                            name="course"
                            rules={[{ required: true, message: "Пожалуйста, введите курс!" }]}
                        >
                            <Input
                                name="course"
                                type="number"
                                value={formData.course}
                                onChange={handleChange}
                                placeholder="Введите курс"
                            />
                        </Form.Item>
                    </>
                )}

                <Form.Item>
                    <Button type="primary" htmlType="submit" loading={loading} block>
                        Зарегистрироваться
                    </Button>
                </Form.Item>
            </Form>
        </div>
    );
};

export default RegistrationForm;