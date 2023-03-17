import {Component, FormEvent, useState} from "react";

type HomeState = {
	status: string,
}

export default class Home extends Component<any, HomeState> {

	constructor(props) {
		super(props);

		this.state = {
			status: "",
		};
	}

	login(event: FormEvent<HTMLFormElement>) {
		const body = {
			username: event.currentTarget.username.value,
			password: event.currentTarget.password.value
		};

		fetch("/api/login", {
			method: "POST",
			headers: {"Content-Type": "application/json"},
			body: JSON.stringify(body)
		})
			.then(res => res.json())
			.then(data => {
				if (data.success) {
					return fetch("/api/tasks");
				} else {
					this.setState({status: data.error});
				}
			})
			.then(res => res.json())
			.then(data => {
				if (data.success) {
					this.setState({status: data.data});
				} else {
					this.setState({status: data.error});
				}
			});
	}

	render() {
		return <div>
			<p>Maintenance</p>
			<form onSubmit={e => {e.preventDefault(); this.login(e);}}>
				<input type="text" name="username" required/>
				<input type="text" name="password" required/>
				<button type="submit">Login</button>
			</form>
			<p>{this.state.status}</p>
		</div>
	}
}
