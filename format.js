const fs = require('fs');
const { join } = require('path');

const formatMenuStructure = list => {
  const newList = list.map(v => {
    const {
      id,
      title,
      isMenu = false,
      outLink = '',
      order = 0,
      label1,
      label2,
      label3,
    } = v;

    const parentId = label3 || label2 || label1 || '';
    const parentIds = [label1, label2, label3].filter(v => !!v);
    const level = [label1, label2, label3].filter(v => !!v).length + 1;

    return {
      id: id,
      label: title,
      href: id,
      isMenu,
      externalLink: outLink,
      parentId,
      parentIds,
      level,
      order,
      children: [],
    };
  });

  newList.sort((x, y) => y.level - x.level);

  const resultList = newList.slice();

  newList.forEach(v => {
    const { parentId } = v;
    const parentIndex = resultList.findIndex(v => v.id === parentId);
    if (parentIndex !== -1) {
      resultList[parentIndex].children.push({
        label: v.label,
        id: v.id,
        isMenu: v.isMenu,
        externalLink: v.externalLink,
        href: v.href,
        children: v.children,
        parentId: parentId,
        parentIds: v.parentIds,
        level: v.level,
      });
    }
  });

  return resultList.filter(v => v.level === 1);
};

const formatMenu = () => {


  const menuPath = join(__dirname, 'site/en/menuStructure/en.json')

  const menu = fs.readFileSync(menuPath, 'utf-8');
  const newMenuStructure = formatMenuStructure(JSON.parse(menu).menuList);

  fs.writeFileSync(menuPath, JSON.stringify(newMenuStructure));
};
formatMenu();
