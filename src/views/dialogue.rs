use crate::blog_book::BookRoute;
use crate::Route;
use dioxus::prelude::*;

const DIALOGUE_CSS: Asset = asset!("/assets/styling/dialogue.css");

/// Post index for markdown pages under `blog-posts/`.
#[component]
pub fn Dialogue() -> Element {
    rsx! {
        document::Link { rel: "stylesheet", href: DIALOGUE_CSS }

        div {
            id: "dialogue",
            h1 { "Dialogue" }
            p { "Posts compiled from markdown at build time." }
            ul { class: "dialogue-list",
                for route in BookRoute::static_routes() {
                    li {
                        Link {
                            to: Route::DialoguePost { child: route },
                            "{route.page().title}"
                        }
                    }
                }
            }
        }
    }
}

/// Layout wrapper around a single generated blog post page.
#[component]
pub fn DialoguePost() -> Element {
    rsx! {
        document::Link { rel: "stylesheet", href: DIALOGUE_CSS }

        div {
            id: "dialogue-post",
            Link {
                to: Route::Dialogue {},
                class: "dialogue-back",
                "Back to dialogue"
            }
            article { class: "dialogue-article markdown-body",
                Outlet::<Route> {}
            }
        }
    }
}
