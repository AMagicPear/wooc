<script setup lang="ts">
import Card from "primevue/card";
import Editor from "primevue/editor";
import { Button, useToast } from "primevue";
import { Form } from "@primevue/forms";
import { onMounted, ref } from "vue";
import CommentCard from "@/components/CommentCard.vue";
import { accountState } from "@/global/account";
import type { Discussion, DiscussionPost } from "@/api/discussion";
import { useRoute } from "vue-router";
import baseApiUrl from "@/api/baseUrl";
import InputText from "primevue/inputtext";
import FloatLabel from "primevue/floatlabel";

const editorValue = ref<string>();
const titleValue = ref<string>();
const courseId = Number(useRoute().params.id);
const discussions = ref<Discussion[]>();
const toast = useToast();
const onDiscussionSubmit = async () => {
  let discussion: DiscussionPost | undefined = undefined;
  if (editorValue.value && titleValue.value) {
    discussion = {
      course_id: courseId,
      title: titleValue.value,
      content: editorValue.value,
      author_id: accountState.userid,
    };
    let postRes = await fetch(new URL("discussion", baseApiUrl));
  } else {
    toast.add({
      severity: "warn",
      summary: "无法提交",
      detail: "请输入话题内容后再提交！",
      life: 3000,
    });
  }
  console.log(discussion);
};

onMounted(async () => {
  let res = await fetch(new URL(`courses/${courseId}/discussions`, baseApiUrl));
  let allDiscussion = await res.json();
  if (allDiscussion.result) {
    discussions.value = allDiscussion.discussions as Discussion[];
  } else {
    console.error(allDiscussion.message);
  }
});
</script>

<template>
  <div id="discussion">
    <Card>
      <template #title>讨论区</template>
      <template #content>
        <p>
          欢迎大家来到讨论区！本讨论区供各位同学就课程问题进行交流学习。请同学们认真阅读下面的【讨论区使用规则】，然后再进行相关发表，谢谢！
        </p>
        <Form @submit="onDiscussionSubmit" class="discussion-form">
          <Editor
            name="content"
            v-model="editorValue"
            editorStyle="height: 120px"
          />
          <FloatLabel variant="on">
            <InputText id="on_label" v-model="titleValue" fluid />
            <label for="on_label">话题标题</label>
          </FloatLabel>
          <Button type="submit" severity="secondary" label="发起新话题" />
        </Form>
      </template>
    </Card>
    <CommentCard
      v-for="discussion in discussions"
      :username="discussion.author_name"
      :content="discussion.content"
      :title="discussion.title"
    />
    <CommentCard
      v-for="discussion in discussions"
      :username="discussion.author_name"
      :content="discussion.content"
      :title="discussion.title"
    />
  </div>
</template>

<style lang="css" scoped>
#discussion {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding-bottom: 20px;
}

.discussion-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
