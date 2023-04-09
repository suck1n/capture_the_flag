import {sessionOptions} from "../../lib/config";
import {withIronSessionApiRoute} from "iron-session/next";
import {NextApiRequest, NextApiResponse} from "next";

export default withIronSessionApiRoute(logoutRoute, sessionOptions);

export type LogoutResponse = {
    success: boolean,
    error?: string
}

async function logoutRoute(req: NextApiRequest, res: NextApiResponse) {
    if (req.method !== "POST") {
        res.status(405).json({ success: false, error: "Method not allowed" } as LogoutResponse);
        return;
    }

    if (!req.session["user"]) {
        res.status(400).json({ success: false, error: "Not logged in"} as LogoutResponse)
    }


    delete req.session["user"]
    await req.session.save();

    res.status(200).send({ success: true } as LogoutResponse);
}