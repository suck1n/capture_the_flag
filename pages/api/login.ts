import {sessionOptions} from "../../lib/config";
import {loginAsUser, User} from "../../lib/database";
import {withIronSessionApiRoute} from "iron-session/next";
import {NextApiRequest, NextApiResponse} from "next";

export default withIronSessionApiRoute(loginRoute, sessionOptions);

export type LoginGetResponse = {
	loggedIn: boolean,
	name: string,
	isGuest: boolean
}

export type LoginPostResponse = {
	success: boolean,
	error?: string
}

type LoginRequest = {
	isGuest: boolean
	username: string
	password: string
}

async function loginRoute(req: NextApiRequest, res: NextApiResponse) {
	if (req.method === "GET") {
		const loggedIn = !!req.session["user"];
		res.status(200).json({ loggedIn: loggedIn, name: loggedIn && req.session["user"].name, isGuest: loggedIn && req.session["user"].guest } as LoginGetResponse);
		return;
	}

	if (req.method !== "POST") {
		res.status(405).json({ success: false, error: "Method not allowed" } as LoginPostResponse);
		return;
	}

	if (!req.headers["content-type"]?.includes("application/json")) {
		res.status(400).json({ success: false, error: "Invalid Content-Type" } as LoginPostResponse);
		return;
	}

	const { isGuest, username, password } = req.body as LoginRequest;

	if ((username === undefined || password === undefined) && isGuest !== true) {
		res.status(200).send({ success: false, error: "User and/or Password can not be empty"} as LoginPostResponse);
		return;
	}

	const user = isGuest ? {
		id: -1,
		name: "Guest",
		guest: true
	} as User : await loginAsUser(username, password);

	if (!user) {
		res.status(200).send({ success: false, error: "User and/or Password was incorrect"} as LoginPostResponse)
		return;
	}

	req.session["user"] = user;
	await req.session.save();

	res.status(200).send({ success: true } as LoginPostResponse);
}