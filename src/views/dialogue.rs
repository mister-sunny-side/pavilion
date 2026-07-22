use crate::Route;
use dioxus::prelude::*;

const DIALOGUE_CSS: Asset = asset!("/assets/styling/dialogue.css");

/// Placeholder posts until markdown-backed content lands.
const POSTS: &[(i32, &str)] = &[
    (1, "Hello, Pavilion"),
    (2, "Notes from the workshop"),
    (3, "Small and fast"),
];

/// The Dialogue tab — index of blog post links.
#[component]
pub fn Dialogue() -> Element {
    rsx! {
        document::Link { rel: "stylesheet", href: DIALOGUE_CSS }

        div {
            id: "dialogue",
            h1 { "Dialogue" }
            p { "Posts and conversations." }
            ul {
                id: "dialogue-posts",
                for (id, title) in POSTS {
                    li {
                        Link {
                            to: Route::Blog { id: *id },
                            "{title}"
                        }
                    }
                }
            }
        }
    }
}
