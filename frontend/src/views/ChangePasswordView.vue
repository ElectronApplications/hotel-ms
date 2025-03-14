<script setup lang="ts">
import PasswordTextField from "@/components/PasswordTextField.vue";
import PrimaryButton from "@/components/PrimaryButton.vue";
import SurfaceCard from "@/components/SurfaceCard.vue";
import { useAuthentication } from "@/composables/auth";
import router from "@/router";
import { useAuthStore } from "@/stores/auth";
import axios, { AxiosError } from "axios";
import { storeToRefs } from "pinia";
import { ref } from "vue";
import { useI18n } from "vue-i18n";

// TODO: this could be a modal dialog

const { t } = useI18n({
  messages: {
    en: {
      changePassword: "Change password",
      oldPassword: "Old password",
      newPassword: "New password",
      confirmNewPassword: "Confirm new password",
      passwordsNotSame: "Passwords do not match",
      passwordShort: "Password must be at least 8 characters long",
      couldntChange: "Couldn't change the password",
    },
    ru: {
      changePassword: "Сменить пароль",
      oldPassword: "Старый пароль",
      newPassword: "Новый пароль",
      confirmNewPassword: "Подтвердите новый пароль",
      passwordsNotSame: "Пароли не совпадают",
      passwordShort: "Пароль должен состоять хотя бы из 8 символов",
      couldntRegister: "Не получилось сменить пароль",
    },
  },
});

const authStore = useAuthStore();
const { currentUser } = storeToRefs(authStore);

const oldPassword = ref("");
const newPassword = ref("");
const newPasswordConfirm = ref("");

const error = ref("");

async function changePassword(): Promise<boolean> {
  if (newPassword.value != newPasswordConfirm.value) {
    error.value = t("passwordsNotSame");
    return false;
  } else if (newPassword.value.length < 8) {
    error.value = t("passwordShort");
    return false;
  }

  try {
    await axios.put("/api/user/password/", {
      old_password: oldPassword.value,
      new_password: newPassword.value,
    });
    await authStore.updateUserInfo();
    router.push("/profile");
    return true;
  } catch (e) {
    error.value = `${t("couldntChange")} (${JSON.stringify((e as AxiosError)?.response?.data)})`;
    return false;
  }
}

useAuthentication((isAuthenticated) => {
  if (!isAuthenticated) {
    router.push("/login");
  }
});
</script>

<template>
  <main class="container mx-auto flex justify-center pt-2">
    <SurfaceCard class="flex flex-col items-center">
      <h1 class="text-2xl font-bold">{{ t("changePassword") }}</h1>
      <span class="text-lg">{{ currentUser?.name }}</span>
      <form class="space-y-4" @submit.prevent="changePassword">
        <div>
          <label for="old-password" class="block text-sm/6 font-medium">{{
            t("oldPassword")
          }}</label>
          <PasswordTextField
            class="mt-2"
            v-model="oldPassword"
            name="old-password"
            :required="true"
          />
        </div>
        <div>
          <label for="password" class="block text-sm/6 font-medium">{{ t("newPassword") }}</label>
          <PasswordTextField class="mt-2" v-model="newPassword" name="password" :required="true" />
        </div>
        <div>
          <label for="confirm-password" class="block text-sm/6 font-medium">{{
            t("confirmNewPassword")
          }}</label>
          <PasswordTextField
            class="mt-2"
            v-model="newPasswordConfirm"
            name="confirm-password"
            :required="true"
          />
        </div>
        <div v-if="error" class="w-[250px] text-wrap break-words">
          <span class="text-primary-light dark:text-primary-dark">{{ error }}</span>
        </div>
        <div>
          <PrimaryButton type="submit" class="w-full">{{ t("changePassword") }}</PrimaryButton>
        </div>
      </form>
    </SurfaceCard>
  </main>
</template>
