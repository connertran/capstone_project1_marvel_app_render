$(".like-unlike").click(likeUnlikePost);
async function likeUnlikePost() {
  try {
    let id = $(this).data("id");
    let $icon = $(this).find("i");
    let $likeCount = $(this).find("span");
    let $likeCountInt = parseInt($likeCount.text());
    if ($icon.hasClass("fa-regular fa-thumbs-up")) {
      await axios.post(`/api/posts/${id}/like`);
      $icon
        .removeClass("fa-regular fa-thumbs-up")
        .addClass("fa-solid fa-thumbs-up");
      $likeCount.text($likeCountInt + 1);
    } else if ($icon.hasClass("fa-solid fa-thumbs-up")) {
      await axios.delete(`/api/posts/${id}/like`);
      $icon
        .removeClass("fa-solid fa-thumbs-up")
        .addClass("fa-regular fa-thumbs-up");
      $likeCount.text($likeCountInt - 1);
    }
  } catch (error) {
    console.error("Error liking/unliking post:", error);
  }
}
