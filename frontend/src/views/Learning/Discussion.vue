<script setup lang="ts">
import Card from "primevue/card";
import Editor from "primevue/editor";
import { Button } from "primevue";
import { Form } from "@primevue/forms";
import { ref } from "vue";

const editorValue = ref<string>();
const onDiscussionSubmit = () => {
    console.log("submit", editorValue.value)
};

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
            editorStyle="height: 200px"
          />
          <Button type="submit" severity="secondary" label="发表评论"/>
        </Form>
      </template>
    </Card>
  </div>
</template>

<style lang="css" scoped>
#discussion {
  margin-top: 20px;
}

.discussion-form{
    display: flex;
    flex-direction: column;
    gap: 10px;
}
</style>
