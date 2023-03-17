import {sessionOptions} from "../../lib/config";
import {loginAsUser} from "../../lib/database";
import {withIronSessionApiRoute} from "iron-session/next";
import {NextApiRequest, NextApiResponse} from "next";

export default withIronSessionApiRoute(loginRoute, sessionOptions);

async function loginRoute(req: NextApiRequest, res: NextApiResponse) {
	if (req.headers["content-type"] !== "application/json" || req.method !== "POST") {
		res.status(400).json("This endpoint only supports post requests with json-data");
		return;
	}

	const username = req.body.username;
	const password = req.body.password;

	if (username === undefined || password === undefined) {
		res.status(200).json({"success": false, "error": "User and/or Password can not be empty"});
		return;
	}

	const user = await loginAsUser(username, password);
	if (!user) {
		res.status(200).json({"success": false, "error": "User and/or Password was incorrect"})
		return;
	}

	req.session["user"] = user;
	await req.session.save();

	res.status(200).json({"success": true});
}