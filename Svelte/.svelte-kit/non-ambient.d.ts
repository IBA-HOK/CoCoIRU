
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
		RouteId(): "/" | "/government" | "/government/communitielist" | "/government/map" | "/government/requestlist" | "/government/requestlist/community" | "/government/requestlist/community/[communityId]" | "/government/requestlist/item" | "/government/requestlist/item/[itemname]" | "/nearby" | "/request";
		RouteParams(): {
			"/government/requestlist/community/[communityId]": { communityId: string };
			"/government/requestlist/item/[itemname]": { itemname: string }
		};
		LayoutParams(): {
			"/": { communityId?: string; itemname?: string };
			"/government": { communityId?: string; itemname?: string };
			"/government/communitielist": Record<string, never>;
			"/government/map": Record<string, never>;
			"/government/requestlist": { communityId?: string; itemname?: string };
			"/government/requestlist/community": { communityId?: string };
			"/government/requestlist/community/[communityId]": { communityId: string };
			"/government/requestlist/item": { itemname?: string };
			"/government/requestlist/item/[itemname]": { itemname: string };
			"/nearby": Record<string, never>;
			"/request": Record<string, never>
		};
		Pathname(): "/" | "/government" | "/government/" | "/government/communitielist" | "/government/communitielist/" | "/government/map" | "/government/map/" | "/government/requestlist" | "/government/requestlist/" | "/government/requestlist/community" | "/government/requestlist/community/" | `/government/requestlist/community/${string}` & {} | `/government/requestlist/community/${string}/` & {} | "/government/requestlist/item" | "/government/requestlist/item/" | `/government/requestlist/item/${string}` & {} | `/government/requestlist/item/${string}/` & {} | "/nearby" | "/nearby/" | "/request" | "/request/";
		ResolvedPathname(): `${"" | `/${string}`}${ReturnType<AppTypes['Pathname']>}`;
		Asset(): "/robots.txt" | string & {};
	}
}