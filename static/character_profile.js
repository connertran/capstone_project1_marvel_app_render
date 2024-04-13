$(".like-unlike").click(likeUnlikeCharacter);
async function likeUnlikeCharacter() {
  try {
    let char_id = $(this).data("id");
    let $icon = $(this).find("i");

    if ($icon.hasClass("fa-solid fa-star")) {
      await axios.delete(`/api/favorite-characters/${char_id}`);
      $icon.removeClass("fa-solid fa-star").addClass("fa-regular fa-star");
      $icon.css("color", "");
    } else if ($icon.hasClass("fa-regular fa-star")) {
      await axios.post(`/api/favorite-characters/${char_id}`);
      $icon.removeClass("fa-regular fa-star").addClass("fa-solid fa-star");
      $icon.css("color", "#ffd43b");
    }
  } catch (error) {
    console.error("Error liking/unliking character:", error);
  }
}
