export const sessionOptions = {
	cookieName: "ctf_session",
	password: process.env.IRON_SESSION_PASSWORD,
	cookieOptions: {
		maxAge: undefined,
		secure: process.env.NODE_ENV === "production",
	},
};