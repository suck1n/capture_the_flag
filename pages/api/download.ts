import {NextApiRequest, NextApiResponse} from "next";
import {withIronSessionApiRoute} from "iron-session/next";
import {sessionOptions} from "../../lib/config";
import {User} from "../../lib/database";
import path from "path";
import {createReadStream, existsSync} from "fs";

export default withIronSessionApiRoute(downloadRoute, sessionOptions);

async function downloadRoute(req: NextApiRequest, res: NextApiResponse) {
    if (req.method !== "GET") {
        res.status(405).json({ error: "Method not allowed" });
        return;
    }

    const user = req.session["user"] as User;

    if (!user) {
        res.status(401).json({ error: "Not logged in" });
        return;
    }

    // if (user.guest) {
    //     res.status(401).json({ error: "Guest user not allowed" });
    //     return;
    // }

    if (!process.env["DOWNLOAD_FOLDER"]) {
        res.status(500).json({ error: "Download folder not defined"});
        return;
    }

    const { file } = req.query;

    if (!file) {
        res.status(404).json({ error: "File can not be empty" });
        return;
    }

    if (file.includes("/") || file.includes("\\") || file.includes("..")) {
        res.status(404).json({ error: "Only file names are allowed"});
        return;
    }

    const filePath = path.join(process.env["DOWNLOAD_FOLDER"], file as string);

    if (!existsSync(filePath)) {
        res.status(404).json({ error: "Not found" });
        return;
    }

    res.setHeader('Content-Type', 'application/zip');
    res.setHeader('Content-Disposition', `attachment; filename=${file}`);

    createReadStream(filePath).pipe(res);
}