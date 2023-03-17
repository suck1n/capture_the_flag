export const sessionOptions = {
	cookieName: "ctf_session",
	password: process.env.IRON_SESSION_PASSWORD,
	cookieOptions: {
		secure: process.env.NODE_ENV === "production",
	},
};