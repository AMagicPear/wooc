<script setup lang="ts">
import { accountState } from "@/global/account";
import { Card } from "primevue";
</script>

<template>
  <div style="padding-top: 20px;">
    <Card>
      <template #content>
        {{ accountState }}
      </template>
    </Card>
  </div>
</template>
