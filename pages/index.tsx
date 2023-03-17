import {Component} from "react";

export default class Home extends Component<any, any> {

	render() {
		return <div>
			<p>Maintenance</p>
			<form action={"/api/login"} method={"post"}>
				<input type={"text"} name={"username"}/>
				<input type={"text"} name={"password"}/>
				<input type={"submit"}/>
			</form>
		</div>
	}
}
