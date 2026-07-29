use dioxus::prelude::*;

/// Returns a random integer generated on the server (0..1_000_000).
#[get("/api/random")]
pub async fn random_number() -> Result<u32> {
    Ok(rand::random::<u32>() % 1_000_000)
}
