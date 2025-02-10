<script setup lang="ts" generic="T">
import { computed, toRefs } from "vue";
import { ChevronUpDownIcon, ChevronUpIcon, ChevronDownIcon } from "@heroicons/vue/24/outline";
import { Popover, PopoverButton, PopoverPanel } from "@headlessui/vue";
import { useI18n } from "vue-i18n";

export type TableCardSlot<T> =
  | {
      isFormRow: true;
    }
  | {
      isFormRow: false;
      data: T;
    };

export type Column = {
  name: string;
  display: string;
} & (
  | { ordering?: boolean; filtering?: undefined }
  | { ordering?: undefined; filtering?: readonly string[] }
);

export type Ordering = {
  name: string;
  order: "ascending" | "descending";
};

export type Filtering = {
  [column: string]: number;
};

const { t } = useI18n({
  messages: {
    en: {
      showingEntries: "Showing {amount} out of {total} entries",
      any: "Any",
    },
    ru: {
      showingEntries: "Отображается {amount} из {total} пунктов",
      any: "Любой",
    },
  },
});

const props = defineProps<{
  columns: Column[];
  rows?: readonly T[];
  extraFormRow?: {
    formName: string;
    formSubmit: () => boolean | Promise<boolean>;
  };
  pagination?: {
    totalPages: number;
    count: number;
  };
}>();

const ordering = defineModel<Ordering>("ordering");
const filtering = defineModel<Filtering>("filtering");
const currentPage = defineModel<number>("currentPage");

const { columns, rows, extraFormRow, pagination } = toRefs(props);

function setOrdering(column: string) {
  if (ordering?.value?.name === column) {
    if (ordering.value.order === "ascending") {
      ordering.value = {
        name: column,
        order: "descending",
      };
    } else {
      ordering.value = undefined;
    }
  } else {
    ordering.value = {
      name: column,
      order: "ascending",
    };
  }
}

function setFiltering(column: string, filter?: number) {
  if (filtering.value === undefined) {
    filtering.value =
      filter !== undefined
        ? {
            [column]: filter,
          }
        : {};
  } else {
    if (filter !== undefined) {
      filtering.value[column] = filter;
    } else {
      delete filtering.value[column];
    }
    filtering.value = Object.assign({}, filtering.value);
  }
}

const pageEntries = computed(() => {
  const current = currentPage.value;
  const total = pagination.value?.totalPages;

  if (current === undefined || total === undefined) {
    return [];
  }

  const pages = new Set(
    [1, 2, current - 1, current, current + 1, total - 1, total].filter((x) => x >= 1 && x <= total)
  );
  const result = [...pages];

  for (let i = 0; i < result.length - 1; i++) {
    if (result[i] + 1 !== result[i + 1]) {
      result.splice(i + 1, 0, -1);
      i += 1;
    }
  }

  return result;
});
</script>

<template>
  <div
    v-if="pagination !== undefined"
    class="flex flex-col items-center space-y-2 lg:flex-row lg:justify-between lg:space-y-0"
  >
    <span>
      {{
        t("showingEntries", {
          amount: rows?.length,
          total: pagination.count,
        })
      }}</span
    >
    <div
      class="flex flex-row overflow-hidden rounded-lg bg-surface-light shadow-md dark:bg-surface-dark"
    >
      <template v-for="[index, entry] in pageEntries.entries()" v-bind:key="index">
        <button v-if="entry !== -1" @click="currentPage = entry">
          <div
            class="px-4 py-2"
            :class="[
              entry === currentPage
                ? 'bg-primary-light text-primary-content-light dark:bg-primary-dark dark:text-primary-content-dark'
                : 'hover:bg-secondary-light hover:text-secondary-content-light dark:hover:bg-secondary-dark dark:hover:text-secondary-content-dark',
            ]"
          >
            {{ entry }}
          </div>
        </button>
        <div v-else class="bg-surface-light px-4 py-2 dark:bg-surface-dark">...</div>
      </template>
    </div>
  </div>

  <div
    class="mt-4 rounded-3xl bg-slate-100 px-0 py-6 text-surface-content-light shadow-md dark:bg-secondary-dark dark:text-surface-content-dark"
  >
    <form
      v-if="extraFormRow !== undefined"
      :id="extraFormRow.formName"
      @submit.prevent="extraFormRow.formSubmit"
    />

    <table class="w-full table-auto bg-slate-100 text-center dark:bg-secondary-dark">
      <thead class="border-b border-secondary-light dark:border-secondary-active-dark">
        <tr>
          <th v-for="column in columns" v-bind:key="column.name" class="py-2">
            <div v-if="column.ordering === true" class="flex w-full flex-row justify-center">
              <button
                class="flex flex-row justify-center space-x-1"
                @click="setOrdering(column.name)"
              >
                <span>{{ column.display }}</span>
                <ChevronUpDownIcon v-if="ordering?.name !== column.name" class="w-[24px]" />
                <ChevronUpIcon v-else-if="ordering.order === 'ascending'" class="w-[24px]" />
                <ChevronDownIcon v-else class="w-[24px]" />
              </button>
            </div>
            <div
              v-else-if="column.filtering !== undefined"
              class="flex w-full flex-row justify-center"
            >
              <Popover class="relative">
                <PopoverButton class="flex flex-col items-center justify-center outline-none">
                  <span class="leading-3">{{ column.display }}</span>
                  <ChevronDownIcon class="w-[16px]" />
                </PopoverButton>

                <transition
                  enter-active-class="transition duration-200 ease-out"
                  enter-from-class="translate-y-1 opacity-0"
                  enter-to-class="translate-y-0 opacity-100"
                  leave-active-class="transition duration-150 ease-in"
                  leave-from-class="translate-y-0 opacity-100"
                  leave-to-class="translate-y-1 opacity-0"
                >
                  <PopoverPanel
                    class="absolute left-1/2 z-10 mt-1 -translate-x-1/2"
                    v-slot="{ close }"
                  >
                    <div
                      class="flex flex-col overflow-hidden rounded-xl bg-surface-light text-surface-content-light shadow-xl dark:bg-surface-dark dark:text-surface-content-dark"
                    >
                      <button
                        class="text-nowrap py-2"
                        :class="[
                          filtering === undefined || filtering[column.name] === undefined
                            ? 'bg-primary-light text-primary-content-light dark:bg-primary-dark dark:text-primary-content-dark'
                            : 'hover:bg-secondary-light hover:text-secondary-content-light dark:hover:bg-secondary-dark dark:hover:text-secondary-content-dark',
                        ]"
                        @click="
                          setFiltering(column.name);
                          close();
                        "
                      >
                        <span class="px-4">{{ t("any") }}</span>
                      </button>
                      <button
                        v-for="[index, filter] in column.filtering.entries()"
                        v-bind:key="index"
                        class="text-nowrap py-2"
                        :class="[
                          filtering !== undefined && filtering[column.name] === index
                            ? 'bg-primary-light text-primary-content-light dark:bg-primary-dark dark:text-primary-content-dark'
                            : 'hover:bg-secondary-light hover:text-secondary-content-light dark:hover:bg-secondary-dark dark:hover:text-secondary-content-dark',
                        ]"
                        @click="
                          setFiltering(column.name, index);
                          close();
                        "
                      >
                        <span class="px-4">
                          {{ filter }}
                        </span>
                      </button>
                    </div>
                  </PopoverPanel>
                </transition>
              </Popover>
            </div>
            <span v-else>{{ column.display }}</span>
          </th>
        </tr>
      </thead>
      <tbody class="bg-surface-light dark:bg-surface-dark">
        <tr v-if="extraFormRow !== undefined">
          <td
            v-for="column in columns"
            v-bind:key="column.name"
            class="border-b border-secondary-light py-4 dark:border-secondary-active-dark"
          >
            <slot :name="column.name" v-bind="{ isFormRow: true } as TableCardSlot<T>"></slot>
          </td>
        </tr>
        <tr v-for="[rowIndex, row] in rows?.entries()" v-bind:key="rowIndex">
          <td
            v-for="column in columns"
            v-bind:key="column.name"
            class="border-b border-secondary-light py-4 dark:border-secondary-active-dark"
          >
            <slot
              :name="column.name"
              v-bind="{ isFormRow: false, data: row } as TableCardSlot<T>"
            ></slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
