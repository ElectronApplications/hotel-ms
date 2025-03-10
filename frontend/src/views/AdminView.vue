<script setup lang="ts">
import DefaultProfileImage from "@/assets/default-profile.png";
import EditableLabel from "@/components/EditableLabel.vue";
import ExpandableImage from "@/components/ExpandableImage.vue";
import PrimaryButton from "@/components/PrimaryButton.vue";
import SelectList from "@/components/SelectList.vue";
import SelectListDynamic from "@/components/SelectListDynamic.vue";
import TextField from "@/components/TextField.vue";
import { useAuthentication, useUserRole } from "@/composables/auth";
import router from "@/router";
import { clientRoles, type Pagination, type Client, type ClientRole } from "@/types";
import { XMarkIcon } from "@heroicons/vue/24/outline";
import axios from "axios";
import { onMounted, ref, watch } from "vue";
import { debounce } from "lodash";
import TableCard, { type Filtering, type Ordering } from "@/components/TableCard.vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n({
  messages: {
    en: {
      hotelClients: "Hotel clients",
      search: "Search",
      name: "Name",
      phoneNumber: "Phone number",
      role: "Role",
      profileImage: "Profile image",
      clientName: "Client's name",
      clientPhoneNumber: "Client's phone number",
      createClient: "Create new client",
      djangoAdmin: "Django admin page",
      stats: "Download statistics",
    },
    ru: {
      hotelClients: "Клиенты отеля",
      search: "Поиск",
      name: "Имя",
      phoneNumber: "Номер телефона",
      role: "Роль",
      profileImage: "Фотография пользователя",
      clientName: "Имя клиента",
      clientPhoneNumber: "Номер телефона клиента",
      createClient: "Создать нового клиента",
      djangoAdmin: "Админка django",
      stats: "Скачать статистику",
    },
  },
});

const clients = ref<Pagination<Client>>();

const clientsPage = ref(1);
const ordering = ref<Ordering>();
const filtering = ref<Filtering>();
const searchKey = ref("");

watch(
  [clientsPage, searchKey, ordering, filtering],
  ([newPage, newSearch], [oldPage, oldSearch]) => {
    if (newPage === oldPage) {
      clientsPage.value = 1;
    }

    if (newSearch !== oldSearch) {
      debouncedFetchClients();
    } else {
      fetchClients();
    }
  }
);

async function fetchClients() {
  let orderingParam = ordering.value?.name;
  if (ordering.value?.order === "descending") {
    orderingParam = `-${orderingParam}`;
  }

  const roleFilter = filtering.value?.role;

  clients.value = (
    await axios.get("/api/client/", {
      params: {
        search: searchKey.value,
        ordering: orderingParam,
        role: roleFilter === undefined ? undefined : clientRoles[roleFilter],
        page: clientsPage.value,
      },
    })
  ).data;
}
const debouncedFetchClients = debounce(fetchClients, 200);

async function changeClientName(client: Client, newName: string) {
  if (client.name !== newName) {
    await axios.patch(`/api/client/${client.id}/`, {
      name: newName,
    });
    await fetchClients();
  }
}

async function changeClientPhoneNumber(client: Client, newPhoneNumber: string) {
  if (client.phone_number !== newPhoneNumber) {
    await axios.patch(`/api/client/${client.id}/`, {
      phone_number: newPhoneNumber,
    });
    await fetchClients();
  }
}

async function changeClientRole(client: Client, newRole: ClientRole) {
  if (client.role !== newRole) {
    await axios.patch(`/api/client/${client.id}/`, {
      role: newRole,
    });
    await fetchClients();
  }
}

async function deleteClient(client: Client) {
  await axios.delete(`/api/client/${client.id}/`);
  await fetchClients();
}

const newClientName = ref("");
const newClientPhoneNumber = ref("");
const newClientRole = ref<number>(clientRoles.indexOf("client"));

async function createClient(): Promise<boolean> {
  if (newClientName.value === "" || newClientPhoneNumber.value === "") {
    return false;
  }

  await axios.post("/api/client/", {
    name: newClientName.value,
    phone_number: newClientPhoneNumber.value,
    role: clientRoles[newClientRole.value],
  });
  await fetchClients();

  newClientName.value = "";
  newClientPhoneNumber.value = "";
  newClientRole.value = clientRoles.indexOf("client");

  return true;
}

async function downloadStats() {
  const response = await axios.get("/api/stats", {
    responseType: "blob",
  });

  const href = URL.createObjectURL(response.data);

  // create "a" HTML element with href to file & click
  const link = document.createElement("a");
  link.href = href;
  document.body.appendChild(link);
  link.click();

  // clean up "a" element & remove ObjectURL
  document.body.removeChild(link);
  URL.revokeObjectURL(href);
}

onMounted(async () => {
  await fetchClients();
});

useAuthentication((isAuthenticated) => {
  if (!isAuthenticated) {
    router.push("/login");
  }
});

useUserRole((role) => {
  if (role !== "admin") {
    router.push("/profile");
  }
});
</script>

<template>
  <main class="container mx-auto pt-4">
    <div class="flex flex-col space-y-4 pb-4 lg:flex-row lg:space-x-4 lg:space-y-0">
      <h1 class="text-center text-4xl font-extrabold lg:text-start">
        {{ t("hotelClients") }}
      </h1>
      <div class="basis-1/3 px-4 lg:px-0">
        <TextField :placeholder="t('search')" v-model="searchKey" @keyup.enter="fetchClients()" />
      </div>
    </div>

    <TableCard
      v-model:ordering="ordering"
      v-model:filtering="filtering"
      v-model:currentPage="clientsPage"
      :columns="[
        { name: 'delete', display: '' },
        { name: 'name', display: t('name'), ordering: true },
        { name: 'phone', display: t('phoneNumber') },
        { name: 'role', display: t('role'), filtering: clientRoles },
        { name: 'image', display: t('profileImage') },
      ]"
      :rows="clients?.results"
      :extraFormRow="{ formName: 'createClientForm', formSubmit: createClient }"
      :pagination="
        clients !== undefined
          ? { totalPages: clients.total_pages, count: clients.count }
          : undefined
      "
    >
      <template #delete="item">
        <button
          v-if="!item.isFormRow && item.data.role !== 'admin'"
          class="rounded-md bg-red-500 p-[4px]"
          @click="deleteClient(item.data)"
        >
          <XMarkIcon class="h-[24px] w-[24px] text-white" />
        </button>
      </template>

      <template #name="item">
        <template v-if="!item.isFormRow">
          <EditableLabel
            v-if="item.data.role !== 'admin'"
            class="justify-center"
            :text="item.data.name"
            @updateText="(value) => changeClientName(item.data, value)"
          />
          <span v-else>
            {{ item.data.name }}
          </span>
        </template>
        <div v-else class="inline-block w-[100px] lg:w-[250px]">
          <TextField
            :placeholder="t('clientName')"
            v-model="newClientName"
            form="createClientForm"
          />
        </div>
      </template>

      <template #phone="item">
        <template v-if="!item.isFormRow">
          <EditableLabel
            v-if="item.data.role !== 'admin'"
            class="justify-center"
            :text="item.data.phone_number"
            @updateText="(value) => changeClientPhoneNumber(item.data, value)"
          />
          <span v-else>
            {{ item.data.phone_number }}
          </span>
        </template>
        <div v-else class="inline-block w-[100px] lg:w-[250px]">
          <TextField
            :placeholder="t('clientPhoneNumber')"
            v-model="newClientPhoneNumber"
            form="createClientForm"
          />
        </div>
      </template>

      <template #role="item">
        <template v-if="!item.isFormRow">
          <SelectListDynamic
            v-if="item.data.role !== 'admin'"
            :options="clientRoles"
            :selected="clientRoles.indexOf(item.data.role)"
            @updateSelection="(value) => changeClientRole(item.data, clientRoles[value])"
          />
          <span v-else>
            {{ item.data.role }}
          </span>
        </template>
        <SelectList
          v-else
          :options="clientRoles"
          :defaultOption="clientRoles.indexOf('client')"
          v-model="newClientRole"
          form="createClientForm"
        />
      </template>

      <template #image="item">
        <ExpandableImage
          v-if="!item.isFormRow"
          imgClass="w-[64px]"
          :src="item.data.picture ?? DefaultProfileImage"
          :alt="item.data.name"
        />
        <PrimaryButton
          v-else
          form="createClientForm"
          type="submit"
          :enabled="newClientName !== '' && newClientPhoneNumber !== ''"
          >{{ t("createClient") }}</PrimaryButton
        >
      </template>
    </TableCard>

    <div class="mt-4">
      <a href="/admin" class="font-bold text-link-light underline dark:text-link-dark">{{
        t("djangoAdmin")
      }}</a>
    </div>

    <div class="mt-4">
      <a
        href="/api/stats/"
        class="font-bold text-link-light underline dark:text-link-dark"
        download
        @click.prevent="downloadStats"
        >{{ t("stats") }}</a
      >
    </div>
  </main>
</template>
