import {Component} from "react";
import {LoginGetResponse} from "./api/login";
import {NextRouter, withRouter} from "next/router";

type IndexState = {
	error?: string
}

type IndexProps = {
	router: NextRouter
}

class Home extends Component<IndexProps, IndexState> {

	constructor(props) {
		super(props);

		this.state = { error: undefined };
	}

	componentDidMount() {
		fetch("/api/login").then(d => d.json())
			.then((data: LoginGetResponse) => {
				if (data.loggedIn) {
					void this.props.router.push("/scoreboard");
				} else {
					void this.props.router.push("/login");
				}
			})
			.catch(err => this.setState({ error: err.toString() }));
	}

	render() {
		if (this.state.error) {
			return <p>An error occurred: <br/> {this.state.error}</p>
		}

		return <p>Loading...</p>
	}
}

export default withRouter(Home);