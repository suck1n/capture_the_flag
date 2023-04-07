import {sessionOptions} from "../../lib/config";
import {loginAsUser} from "../../lib/database";
import {withIronSessionApiRoute} from "iron-session/next";
import {NextApiRequest, NextApiResponse} from "next";

export default withIronSessionApiRoute(loginRoute, sessionOptions);

interface LoginForm {
	username: string;
	password: string;
}

async function loginRoute(req: NextApiRequest, res: NextApiResponse) {
	if (req.method !== "POST") {
		res.status(405).json({ success: false, error: "Method not allowed" });
		return;
	}

	if (!req.headers["content-type"]?.includes("application/json")) {
		res.status(400).json({ success: false, error: "Invalid Content-Type" });
		return;
	}

	const { username, password } = req.body as LoginForm;

	if (username === undefined || password === undefined) {
		res.status(200).send({ success: false, error: "User and/or Password can not be empty"});
		return;
	}

	const user = await loginAsUser(username, password);
	if (!user) {
		res.status(200).send({ success: false, error: "User and/or Password was incorrect"})
		return;
	}

	req.session["user"] = user;
	await req.session.save();

	res.status(200).send({ success: true });
}