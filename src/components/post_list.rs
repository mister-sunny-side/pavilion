use crate::blog_book::BookRoute;
use crate::components::PostLink;
use dioxus::prelude::*;

/// Renders every build-time blog route as a list of [`PostLink`]s.
#[component]
pub fn PostList() -> Element {
    rsx! {
        ul { class: "dialogue-list",
            for route in BookRoute::static_routes() {
                li {
                    PostLink { route }
                }
            }
        }
    }
}
