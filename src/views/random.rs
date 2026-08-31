use dioxus::prelude::*;

use crate::server::random_number;

/// Random page backed by a server function.
#[component]
pub fn Random() -> Element {
    let mut roll_key = use_signal(|| 0u32);
    let number = use_server_future(move || {
        let _ = roll_key();
        random_number()
    })?;

    rsx! {
        div {
            id: "random",
            class: "page page-center",
            h1 { "Random" }
            p { "This number was generated on the server:" }
            match number() {
                Some(Ok(value)) => rsx! {
                    p {
                        id: "random-number",
                        class: "random-number",
                        "{value}"
                    }
                },
                Some(Err(err)) => rsx! {
                    p { id: "random-error", "Could not fetch a random number: {err}" }
                },
                None => rsx! {
                    p { id: "random-loading", "Rolling..." }
                },
            }
            button {
                id: "random-roll",
                r#type: "button",
                onclick: move |_| *roll_key.write() += 1,
                "Roll again"
            }
        }
    }
}
