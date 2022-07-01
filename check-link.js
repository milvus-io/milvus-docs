const fs = require("fs");
const path = require("path");

const EN_MENU_PATH = path.join(__dirname, "site/en/menuStructure/en.json");
const EN_MDS_PATH = path.join(__dirname, "site/en/");

const errors = [];
const getMenuJson = (path) => {
  const doc = fs.readFileSync(path);
  return JSON.parse(doc.toString());
};

const EN_MENU_CONTENT = getMenuJson(EN_MENU_PATH);
const enIds = EN_MENU_CONTENT.menuList.map((v) => v.id);

// check if id is duplicate in menustructor
const checkSameId = (ids, prefix = "") => {
  const arr = [];
  const sameArr = new Set();
  ids.forEach((v) => {
    arr.includes(v) ? sameArr.add(v) : arr.push(v);
  });
  if (sameArr.size > 0) {
    let warning = "";
    sameArr.forEach(
      (v) =>
        (warning += `Menustructure ${prefix}.json - id: ${
          v || `\'\'`
        } is duplicate. \n`)
    );
    errors.push(warning);
    // throw new Error(warning);
  }
  return "";
};

checkSameId(enIds, "EN");

const metaRegx = /(\S+)\s*?:\s*([\s\S]*?)(?=$|\n)/g;
/**
 *
 * @param {*} dirPath
 * @param {*} validMds
 * @param {*} validPaths
 * @returns {
 * validMds: all valid markdown id
 * validPaths: all valid markdown file path
 * }
 */
const generateValidIds = (dirPath, validMds = [], validPaths = []) => {
  let filesList = fs.readdirSync(dirPath);
  for (let i = 0; i < filesList.length; i++) {
    //拼接当前文件的路径(上一层路径+当前file的名字)
    let filePath = path.join(dirPath, filesList[i]);
    //根据文件路径获取文件信息，返回一个fs.Stats对象
    let stats = fs.statSync(filePath);
    if (stats.isDirectory()) {
      //递归调用
      generateValidIds(filePath, validMds, validPaths);
    } else {
      if (filesList[i].includes(".md") && !dirPath.includes("fragments")) {
        const doc = fs.readFileSync(filePath);
        const content = doc.toString();
        const match = content.match(metaRegx);
        if (match && match[0].includes("id")) {
          const metaId = match[0].split(":")[1].trim();
          if (metaId !== filesList[i]) {
            errors.push(`Filename: ${filesList[i]} need same with its id`);
            // throw `Filename: ${filesList[i]} need same with its id`;
          }
          validMds.push(metaId);
          validPaths.push(filePath);
        }
      }
    }
  }
  return { validMds, validPaths };
};

const { validMds: enValidMds, validPaths: enValidPaths } =
  generateValidIds(EN_MDS_PATH);


const enMenuMdIds = enIds.filter((v) => v.includes(".md"));

const checkIsIdValid = (arr, validArr) => {
  arr.forEach((v) => {
    if (!validArr.includes(v)) {
      errors.push(
        `Id: ${v} in menustructor will be a broken link, because cant find markdown file by this id. `
      );
      // throw new Error(
      //   `Id: ${v} in menustructor will be a broken link, because cant find markdown file by this id. `
      // );
    }
  });
};

// check menu id valid
checkIsIdValid(enMenuMdIds, enValidMds);

const linkRegx = /[^(\]\()]+(?=\))/g;
const checkInnerLink = (paths, validMds) => {
  paths.forEach((v) => {
    const doc = fs.readFileSync(v);
    const content = doc.toString();
    const match = content.match(linkRegx);
    const innerLinks = match
      ? match.filter(
          (v) =>
            v && v.includes(".md") && !v.includes("http") && !v.includes("\n")
        )
      : [];
    innerLinks.forEach((link) => {
      let ignoreAnchorLink = link.split("#")[0];
      // ignore api reference
      if (link.includes("/api-reference/")) {
        return;
      }
      if (!validMds.includes(ignoreAnchorLink)) {
        errors.push(`Check Link ${link} in ${v}`);
        // throw new Error(`Check Link ${link} in ${v}`);
      }
    });
  });
};

// check markdown file inner link
checkInnerLink(enValidPaths, enValidMds);

if (errors.length) {
  errors.forEach((v) => console.log(v));
  throw new Error("Fail");
}
