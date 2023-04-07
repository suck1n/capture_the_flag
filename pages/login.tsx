import React from "react";
import {NextRouter, withRouter} from "next/router";

interface LoginForm {
    username: string;
    password: string;
}

interface LoginResponse {
    success: boolean;
    error?: string;
}

interface LoginProps {
    router: NextRouter;
}

class Login extends React.Component<LoginProps, LoginForm> {
    state = { username: "", password: "" };
    private error = "";

    handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = event.target;
        this.setState((prev) => ({ ...prev, [name]: value }));
    };

    handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        try {
            const response = await fetch("/api/login", {
                method: "POST",
                headers: {"Content-Type": "application/json",},
                body: JSON.stringify(this.state),
            });

            const data: LoginResponse = await response.json();

            if (data.success) {
                await this.props.router.push("/");
            } else {
                this.error = data.error;
                this.forceUpdate();
            }
        } catch (error) {
            console.error(error);
            this.error = "An error occurred while logging in";
            this.forceUpdate();
        }
    };

    render() {
        return (
            <div>
                <h1>Login</h1>
                <form onSubmit={this.handleSubmit}>
                    <label>
                        Username:
                        <input
                            type="text"
                            name="username"
                            value={this.state.username}
                            onChange={this.handleInputChange}
                        />
                    </label>
                    <br />
                    <label>
                        Password:
                        <input
                            type="password"
                            name="password"
                            value={this.state.password}
                            onChange={this.handleInputChange}
                        />
                    </label>
                    <br />
                    <button type="submit">Login</button>
                    {this.error && <p>{this.error}</p>}
                </form>
            </div>
        );
    }
}

export default withRouter(Login);