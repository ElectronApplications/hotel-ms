<script setup lang="ts">
import SurfaceCard from "@/components/SurfaceCard.vue";
import BrandIcon from "@/assets/brand-icon.svg";
import router from "@/router";
import { useAuthStore } from "@/stores/auth";
import { ref } from "vue";
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from "@headlessui/vue";
import PrimaryButton from "@/components/PrimaryButton.vue";
import TextField from "@/components/TextField.vue";
import PasswordTextField from "@/components/PasswordTextField.vue";
import { useAuthentication } from "@/composables/auth";
import axios, { AxiosError } from "axios";
import { useI18n } from "vue-i18n";

const { t } = useI18n({
  messages: {
    en: {
      login: "Login",
      register: "Register",
      signIn: "Sign in",
      signUp: "Sign up",
      name: "Name",
      phoneNumber: "Phone number",
      password: "Password",
      confirmPassword: "Confirm password",
      incorrectNumberPassword: "Incorrect phone number or password",
      passwordsNotSame: "Passwords do not match",
      passwordShort: "Password must be at least 8 characters long",
      couldntRegister: "Couldn't complete registration",
    },
    ru: {
      login: "Вход",
      register: "Регистрация",
      signIn: "Войти",
      signUp: "Зарегистрироваться",
      name: "Имя",
      phoneNumber: "Номер телефона",
      password: "Пароль",
      confirmPassword: "Подтвердите пароль",
      incorrectNumberPassword: "Неправильный номер телефона или пароль",
      passwordsNotSame: "Пароли не совпадают",
      passwordShort: "Пароль должен состоять хотя бы из 8 символов",
      couldntRegister: "Не получилось зарегистрироваться",
    },
  },
});

const authStore = useAuthStore();

const loginPhoneNumber = ref("");
const loginPassword = ref("");
const loginError = ref<string>();

const registerName = ref("");
const registerPhoneNumber = ref("");
const registerPassword = ref("");
const registerConfirmPassword = ref("");
const registerError = ref<string>();

async function loginSubmit(): Promise<boolean> {
  const result = await authStore.login(loginPhoneNumber.value, loginPassword.value);

  if (!result) {
    loginError.value = t("incorrectNumberPassword");
  }
  return result;
}

async function registerSubmit(): Promise<boolean> {
  if (registerPassword.value !== registerConfirmPassword.value) {
    registerError.value = t("passwordsNotSame");
    return false;
  } else if (registerPassword.value.length < 8) {
    registerError.value = t("passwordShort");
    return false;
  }

  try {
    await axios.post("/api/user/", {
      name: registerName.value,
      phone_number: registerPhoneNumber.value,
      password: registerPassword.value,
    });
    await authStore.login(registerPhoneNumber.value, registerPassword.value);
    return true;
  } catch (e) {
    registerError.value = `${t("couldntRegister")} (${JSON.stringify((e as AxiosError)?.response?.data)})`;
    return false;
  }
}

useAuthentication((isAuthenticated) => {
  if (isAuthenticated) {
    router.push("/profile");
  }
});
</script>

<template>
  <main class="container mx-auto flex justify-center pt-2">
    <SurfaceCard class="flex flex-col items-center">
      <BrandIcon class="scale-150" />

      <div class="pt-6">
        <TabGroup>
          <TabList
            class="flex w-[300px] flex-row space-x-1 rounded-xl bg-primary-light p-1 dark:bg-primary-dark"
          >
            <Tab v-slot="{ selected }" class="basis-1/2 outline-none"
              ><button
                class="w-full rounded-lg py-2"
                :class="[
                  selected
                    ? 'bg-surface-light text-surface-content-light shadow dark:bg-surface-dark dark:text-surface-content-dark'
                    : 'text-primary-content-light hover:bg-primary-active-light dark:text-primary-content-dark dark:hover:bg-primary-active-dark',
                ]"
              >
                {{ t("login") }}
              </button></Tab
            >

            <Tab v-slot="{ selected }" class="basis-1/2 outline-none"
              ><button
                class="w-full rounded-lg py-2"
                :class="[
                  selected
                    ? 'bg-surface-light text-surface-content-light shadow dark:bg-surface-dark dark:text-surface-content-dark'
                    : 'text-primary-content-light hover:bg-primary-active-light dark:text-primary-content-dark dark:hover:bg-primary-active-dark',
                ]"
              >
                {{ t("register") }}
              </button></Tab
            >
          </TabList>

          <TabPanels class="pt-4">
            <TabPanel>
              <form class="space-y-4" @submit.prevent="loginSubmit">
                <div>
                  <label for="phone_number" class="block text-sm/6 font-medium">{{
                    t("phoneNumber")
                  }}</label>
                  <TextField
                    class="mt-2"
                    v-model="loginPhoneNumber"
                    name="phone_number"
                    type="tel"
                    autocomplete="tel"
                    :required="true"
                  />
                </div>
                <div>
                  <label for="password" class="block text-sm/6 font-medium">{{
                    t("password")
                  }}</label>
                  <PasswordTextField
                    class="mt-2"
                    v-model="loginPassword"
                    name="password"
                    :required="true"
                  />
                </div>
                <div v-if="loginError">
                  <span class="text-primary-light dark:text-primary-dark">{{ loginError }}</span>
                </div>
                <div>
                  <PrimaryButton type="submit" class="w-full">
                    {{ t("signIn") }}
                  </PrimaryButton>
                </div>
              </form>
            </TabPanel>

            <TabPanel>
              <form class="space-y-4" @submit.prevent="registerSubmit">
                <div>
                  <label for="name" class="block text-sm/6 font-medium">{{ t("name") }}</label>
                  <TextField
                    class="mt-2"
                    v-model="registerName"
                    name="name"
                    type="text"
                    autocomplete="name"
                    :required="true"
                  />
                </div>
                <div>
                  <label for="phone_number" class="block text-sm/6 font-medium">{{
                    t("phoneNumber")
                  }}</label>
                  <TextField
                    class="mt-2"
                    v-model="registerPhoneNumber"
                    name="phone_number"
                    type="tel"
                    autocomplete="tel"
                    :required="true"
                  />
                </div>
                <div>
                  <label for="password" class="block text-sm/6 font-medium">{{
                    t("password")
                  }}</label>
                  <PasswordTextField
                    class="mt-2"
                    v-model="registerPassword"
                    name="password"
                    :required="true"
                  />
                </div>
                <div>
                  <label for="confirm-password" class="block text-sm/6 font-medium">{{
                    t("confirmPassword")
                  }}</label>
                  <PasswordTextField
                    class="mt-2"
                    v-model="registerConfirmPassword"
                    name="confirm-password"
                    :required="true"
                  />
                </div>
                <div v-if="registerError" class="max-w-[250px] text-wrap break-words">
                  <span class="text-primary-light dark:text-primary-dark">
                    {{ registerError }}
                  </span>
                </div>
                <div>
                  <PrimaryButton type="submit" class="w-full">
                    {{ t("signUp") }}
                  </PrimaryButton>
                </div>
              </form>
            </TabPanel>
          </TabPanels>
        </TabGroup>
      </div>
    </SurfaceCard>
  </main>
</template>
