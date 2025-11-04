
// this file is generated — do not edit it


declare module "svelte/elements" {
	export interface HTMLAttributes<T> {
		'data-sveltekit-keepfocus'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-noscroll'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-preload-code'?:
			| true
			| ''
			| 'eager'
			| 'viewport'
			| 'hover'
			| 'tap'
			| 'off'
			| undefined
			| null;
		'data-sveltekit-preload-data'?: true | '' | 'hover' | 'tap' | 'off' | undefined | null;
		'data-sveltekit-reload'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-replacestate'?: true | '' | 'off' | undefined | null;
	}
}

export {};


declare module "$app/types" {
	export interface AppTypes {
		RouteId(): "/" | "/government" | "/government/communitielist" | "/government/requestlist" | "/nearby" | "/request" | "/request/confirm";
		RouteParams(): {
			
		};
		LayoutParams(): {
			"/": Record<string, never>;
			"/government": Record<string, never>;
			"/government/communitielist": Record<string, never>;
			"/government/requestlist": Record<string, never>;
			"/nearby": Record<string, never>;
			"/request": Record<string, never>;
			"/request/confirm": Record<string, never>
		};
		Pathname(): "/" | "/government" | "/government/" | "/government/communitielist" | "/government/communitielist/" | "/government/requestlist" | "/government/requestlist/" | "/nearby" | "/nearby/" | "/request" | "/request/" | "/request/confirm" | "/request/confirm/";
		ResolvedPathname(): `${"" | `/${string}`}${ReturnType<AppTypes['Pathname']>}`;
		Asset(): "/robots.txt" | string & {};
	}
}