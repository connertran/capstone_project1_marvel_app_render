$(".like-unlike").click(likeUnlikeCharacter);
async function likeUnlikeCharacter() {
  try {
    let char_id = $(this).data("id");
    let $icon = $(this).find("i");

    if ($icon.hasClass("fa-solid fa-star")) {
      await axios.delete(`/api/favorite-characters/${char_id}`);
      $(this).closest(".character-div").remove();
    }
  } catch (error) {
    console.error("Error liking/unliking post:", error);
  }
}
