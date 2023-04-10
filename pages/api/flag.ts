import {NextApiRequest, NextApiResponse} from "next";
import {withIronSessionApiRoute} from "iron-session/next";
import {sessionOptions} from "../../lib/config";
import {claimFlag, getFlag, User} from "../../lib/database";

export default withIronSessionApiRoute(flagRoute, sessionOptions);

export type FlagResponse = {
    success: boolean
    error?: string
}

type FlagRequest = {
    flag: string
}

async function flagRoute(req: NextApiRequest, res: NextApiResponse) {
    if (req.method !== "POST") {
        res.status(405).json({ success: false, error: "Method not allowed" } as FlagResponse);
        return;
    }

    if (!req.headers["content-type"]?.includes("application/json")) {
        res.status(400).json({ success: false, error: "Invalid Content-Type" } as FlagResponse);
        return;
    }

    const user = req.session["user"] as User;

    if (!user) {
        res.status(401).json({ success: false, error: "Not logged in" } as FlagResponse);
        return;
    }

    const flagString = (req.body as FlagRequest).flag;

    if (!flagString) {
        res.status(200).send({ success: false, error: "Flag can not be empty"} as FlagResponse);
        return;
    }

    console.log("1");
    const flag = await getFlag(flagString);
    console.log("2");

    if (!flag) {
        res.status(200).send({ success: false, error: "Flag does not exist"} as FlagResponse);
        return;
    }

    console.log("3");
    if (flag.claimed) {
        res.status(200).send({ success: false, error: "Flag already claimed"} as FlagResponse);
        return;
    }

    console.log(user.id);

    console.log("4");
    await claimFlag(user.id, flag.flag);
    console.log("5");

    res.status(200).send({ success: true } as FlagResponse);
}