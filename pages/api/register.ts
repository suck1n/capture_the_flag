import {sessionOptions} from "../../lib/config";
import {createUser, userExists} from "../../lib/database";
import {withIronSessionApiRoute} from "iron-session/next";
import {NextApiRequest, NextApiResponse} from "next";

export default withIronSessionApiRoute(registerRoute, sessionOptions);

export type RegisterResponse = {
    success: boolean,
    error?: string
}

type RegisterRequest = {
    username: string;
    password: string;
}

async function registerRoute(req: NextApiRequest, res: NextApiResponse) {
    if (req.method !== "POST") {
        res.status(405).json({ success: false, error: "Method not allowed" } as RegisterResponse);
        return;
    }

    if (!req.headers["content-type"]?.includes("application/json")) {
        res.status(400).json({ success: false, error: "Invalid Content-Type" } as RegisterResponse);
        return;
    }

    const { username, password } = req.body as RegisterRequest;

    if (username === undefined || password === undefined) {
        res.status(200).send({ success: false, error: "User and/or Password can not be empty"} as RegisterResponse);
        return;
    }

    if (await userExists(username)) {
        res.status(200).send({ success: false, error: "Username is already taken"});
        return;
    }

    await createUser(username, password);
    res.status(200).send({ success: true } as RegisterResponse);
}