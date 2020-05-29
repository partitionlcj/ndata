<template>
  <Layout class="layout">
    <Sider ref="side1" hide-trigger collapsible :collapsed-width="78" v-model="isCollapsed">
      <div class="logo-text" style="border-bottom: 1px solid hsla(0,0%,71%,.3)" :style="{fontSize: isCollapsed ? '12px': '28px'}">NDATA</div>
      <Menu active-name="1-2" theme="dark" width="auto" :class="menuitemClasses">
        <MenuGroup v-for="(menu, index) in menu" :title="!isCollapsed ? menu.label :''" :key="index">
          <template v-for="(subMenu, index) in menu.children">
            <router-link :to="subMenu.to" :key="index">
              <Tooltip :content="subMenu.label" placement="right" style="width:100%" :disabled="!isCollapsed">
                <MenuItem :name="subMenu.name">
                <Icon :type="subMenu.icon" size="24" />
                <template v-if="!isCollapsed">{{subMenu.label}}</template>
                </MenuItem>
              </Tooltip>
            </router-link>
          </template>
        </MenuGroup>
      </Menu>
    </Sider>
    <Layout class="content">
      <Header :style="{padding: 0}" class="layout-header-bar">
        <div>
          <Icon @click.native="collapsedSider" :class="rotateIcon" :style="{margin: '0 20px'}" type="md-menu" size="24"></Icon>
          <label class="label-text" v-html="labelText"></label>
        </div>
        <div class="display-inline-block" :style="{margin: '0 20px'}">
          <Icon type="ios-person" size="24" />
          <label style="font-size: 16px">{{user}}</label>
          <Icon @click.native="logout" type="md-log-out" size="24" style="cursor: pointer;" />
        </div>
      </Header>
      <Content style="margin: 20px; padding: 10px; background: #fff;">
        <router-view keep-alive></router-view>
      </Content>
    </Layout>
  </Layout>
</template>
<script>
import { mapState } from 'vuex';

export default {
  data() {
    return {
      isCollapsed: true
    }
  },
  computed: {
    rotateIcon() {
      return [
        'menu-icon',
        this.isCollapsed ? 'rotate-icon' : ''
      ];
    },
    menuitemClasses() {
      return [
        'sariel-menu',
        'menu-item',
        this.isCollapsed ? 'collapsed-menu' : ''
      ]
    },
    ...mapState({
      crumbs: state => state.menu.crumb,
      user: state => state.user.name,
      role: state => state.user.role,
      menu: state => state.menu.menu,
      labelText: state => state.menu.labelText
    })
  },
  methods: {
    collapsedSider() {
      this.$refs.side1.toggleCollapse();
    },
    logout() {
      this.$store.commit('LOGOUT');
      this.$Modal.success({
        title: '退出登录提示',
        content: '退出成功，感谢您的使用～～',
        onOk: () => {
          document.location = "/"
        }
      });
    }
  }
}

</script>
<style scoped>
.layout {
  border: 1px solid #d7dde4;
  background: #f5f7f9;
  position: relative;
  border-radius: 4px;
  overflow: hidden;
  height: 100vh;
}

.layout-header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
  box-shadow: 0 1px 1px rgba(0, 0, 0, .1);
}

.layout-logo-left {
  width: 90%;
  height: 30px;
  background: #5b6270;
  border-radius: 3px;
  margin: 15px auto;
}

.menu-icon {
  transition: all .3s;
}

.rotate-icon {
  transform: rotate(-90deg);
}

.menu-item span {
  display: inline-block;
  overflow: hidden;
  width: 69px;
  text-overflow: ellipsis;
  white-space: nowrap;
  vertical-align: bottom;
  transition: width .2s ease .2s;
}

.menu-item i {
  transform: translateX(0px);
  transition: font-size .2s ease, transform .2s ease;
  vertical-align: middle;
  font-size: 16px;
}

.collapsed-menu span {
  width: 0px;
  transition: width .2s ease;
}

.collapsed-menu i {
  transform: translateX(5px);
  transition: font-size .2s ease .2s, transform .2s ease .2s;
  vertical-align: middle;
  font-size: 22px;
}

.logo-text {
  width: 90%;
  color: rgba(255, 255, 255, .7);
  margin: 20px auto;
  text-align: center;
  margin-left: auto;
  margin-right: auto;
  padding-bottom: 10px;
}

.sariel-menu>>>.ivu-menu-item:hover,
.sariel-menu>>>.ivu-menu-item-active:hover {
  background-color: #00bebe;
}

</style>
